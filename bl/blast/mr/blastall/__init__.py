# BEGIN_COPYRIGHT
# END_COPYRIGHT
"""
Sequence alignment based on a wrapper for the blastall program.
"""

from pydoop.pipes import runTask, Factory
from bl.core.seq.mr.fasta_reader import record_reader
from mapper import Mapper
from reducer import Reducer


def run_task():
  return runTask(Factory(Mapper, Reducer, record_reader))
