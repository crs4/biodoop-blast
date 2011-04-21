# BEGIN_COPYRIGHT
# END_COPYRIGHT
import os, logging, zlib
logging.basicConfig(level=logging.DEBUG)

import pydoop.pipes as pp
import pydoop.utils as pu
from bl.core.seq.engines.blastall_2_2_21 import Engine


class Mapper(pp.Mapper):
  """
  Maps query sequences to blastall results.

  @input-record: C{key} = fasta header, C{value} = sequence.

  @output-record: tabular result of blastall against the specified db.

  @jobconf-param: C{bl.mr.seq.blastall.log.level} logging level,
  specified as a logging module literal; defaults to 'WARNING'.

  @jobconf-param: C{bl.mr.seq.blastall.db.name} The BLAST database
  name (REQUIRED). A BLAST db is typically obtained by running the
  C{formatdb} command on one or more fasta files. The archive provided
  through C{mapred.cache.archives} MUST contain BLAST db files
  beginning with the db name (DB_NAME.nin, etc.).

  @jobconf-param: C{bl.mr.seq.blastall.program} The BLAST program
  to use ('blastn', 'blastp', etc.); defaults to 'blastn'.
  
  @jobconf-param: C{mapred.cache.archives} distributed cache entry
  (HDFS_PATH#LINK_NAME) for an archive containing the pre-formatted db
  files at the top level, i.e., no directories.

  @jobconf-param: C{mapred.create.symlink} must be set to 'yes'.
  """
  COUNTER_CLASS = "BLASTALL"

  def __get_configuration(self, jc):
    pu.jc_configure(self, jc, 'bl.mr.seq.blastall.log.level',
                    'log_level', 'WARNING')
    try:
      self.log_level = getattr(logging, self.log_level)
    except AttributeError:
      raise ValueError("Unsupported log level: %r" % self.log_level)
    pu.jc_configure(self, jc, 'bl.mr.seq.blastall.program',
                    'program', 'blastn')
    pu.jc_configure(self, jc, 'bl.mr.seq.blastall.db.name', 'db_name')
    pu.jc_configure_bool(self, jc, 'bl.mr.fasta-reader.compress.header',
                         'compress_header', False)
    pu.jc_configure_bool(self, jc, 'bl.mr.fasta-reader.compress.seq',
                         'compress_seq', True)

  def __init__(self, ctx):
    super(Mapper, self).__init__(ctx)
    self.ctx = ctx
    jc = self.ctx.getJobConf()
    self.__get_configuration(jc)
    self.hit_counter = self.ctx.getCounter(self.COUNTER_CLASS, "BLAST_HITS")
    self.logger = logging.getLogger("mapper")
    self.logger.setLevel(self.log_level)
    self.input_file = "temp.in"
    self.output_file = "temp.out"
    engine_logger = logging.getLogger("blastall")
    engine_logger.setLevel(self.log_level)
    self.engine = Engine(logger=engine_logger)
    try:
      self.db_dir = jc.get("mapred.cache.archives").split(",")[0].split("#")[1]
    except IndexError:
      raise ValueError('bad format for "mapred.cache.archives"')
    self.opts = {
      "blastall.program": self.program,
      "blastall.database": os.path.join(self.db_dir, self.db_name),
      "blastall.out.tabular": True,
      "blastall.input.file": self.input_file,
      "blastall.output.file": self.output_file,
      }

  def map(self, ctx):
    header, seq = ctx.getInputKey(), ctx.getInputValue()
    if self.compress_header:
      header = zlib.decompress(header)
    if self.compress_seq:
      seq = zlib.decompress(seq)

    # TODO: use stdin/stdout instead
    self.__write_input(header, seq)
    self.engine.blastall(opts=self.opts)
    for result in self.__read_output():
      ctx.incrementCounter(self.hit_counter, 1)
      k, v = result.split("\t", 1)
      ctx.emit(k, v)

  def __write_input(self, header, seq):
    f = open(self.input_file, "w")
    f.write(">%s\n%s\n" % (header, seq))
    f.close()

  def __read_output(self):
    f = open(self.output_file)
    for line in f:
      yield line.rstrip()
    f.close()
