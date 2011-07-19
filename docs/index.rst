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

#. unpack the biodoop-blast tarball, move to the distribution directory
   and run::

     python setup.py install

   for a system-wide installation, or::

     python setup.py install --user

   for a local installation
