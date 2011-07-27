.. _index:

Biodoop-BLAST
=============

Biodoop-BLAST is a wrapper-based MapReduce implementation of BLAST for
Hadoop. It is based on `Biodoop's core component
<http://biodoop.sourceforge.net>`_, in turn based on the `Pydoop
<http://pydoop.sourceforge.net>`_ API for `Hadoop
<http://hadoop.apache.org>`_.

Installation:

#. install `Biodoop core <http://biodoop.sourceforge.net>`_

#. get biodoop-blast from the `download page <https://sourceforge.net/projects/biodoop/files/>`_

#. unpack the biodoop-blast tarball, move to the distribution directory
   and run::

     python setup.py install

   for a system-wide installation, or::

     python setup.py install --user

   for a local installation


Usage
-----

Here is a quick usage example that can be run on a laptop:

.. code-block:: bash

  $ start-all.sh
  $ hadoop dfsadmin -safemode wait
  $ wget ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/chromosomes/*random*
  $ zcat chr*.gz >genome
  $ formatdb -p F -o T -i genome
  $ tar cf genome.tar genome.*
  $ cat >query.fa
  >q1
  ATCGCCTCTCCCGACCGAGCCTTCATGGGAGTCCCGCGGGAGCTGCTCCC
  >q2
  TAGAAACTTGCTATTTCAAGTATTGTCATCACCTGGGATCTTGCTCGAAT
  $ biodoop_blast -o output.csv -p blastn -d genome query.fa genome.tar
