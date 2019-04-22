.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.dos.anjos@gmail.com>
.. Fri 16 May 11:48:13 2014 CEST

.. include:: links.rst
.. testsetup:: *

   current_directory = os.path.realpath(os.curdir)
   temp_dir = tempfile.mkdtemp(prefix='bob_doctest_')
   os.chdir(temp_dir)

============
 User Guide
============

By importing this package, you can use several utilities to make easier your the installation and start-up of your research bob projects


Accesses
--------

TODO

Databases (Interface)
----------------------

TODO


Evaluation
----------

TODO

Features Extractor (Interface)
------------------------------

TODO

Informer
--------

TODO

Multiprocess
------------

TODO

Storage
-------

TODO


.. testcleanup:: *

  import shutil
  os.chdir(current_directory)
  shutil.rmtree(temp_dir)