.. vim: set fileencoding=utf-8 :
.. Gradiant's Biometrics Team <biometrics.support@gradiant.org>
.. Copyright (C) 2017 Gradiant, Vigo, Spain

============
 Python API
============

This section includes information for using the pure Python API of
``bob.gradiant.core``.


.. automodule:: bob.gradiant.core

Accesses
--------

.. autoclass:: Access
    :members:

.. autoclass:: FolderAccess
    :members:

.. autoclass:: VideoAccess
    :members:

.. autoclass:: AccessModificator
    :members:

.. autoclass:: FramerateModificator
    :members:

.. autoclass:: TimestampNormalizer
    :members:

.. autoclass:: Trimmer
    :members:

.. autoclass:: DataAugmentator
    :members:

Databases (Interface)
----------------------

TODO

.. autoclass:: Database
    :members:

.. autoclass:: TypeDatabase
    :members:

Evaluation
----------

Data
====

.. autoclass:: Performance
    :members:

.. autoclass:: PerformanceContainer
    :members:

.. autoclass:: PerformanceExtractor
    :members:

Metrics
=======

.. autoclass:: Metric
    :members:

.. autoclass:: Acer
    :members:

.. autoclass:: Apcer
    :members:

.. autoclass:: Bpcer
    :members:

.. autoclass:: Auc
    :members:

.. autoclass:: Eer
    :members:

.. autoclass:: Far
    :members:

.. autoclass:: Hter
    :members:


Features Extractor (Interface)
------------------------------

.. autoclass:: FeaturesExtractor
    :members:

.. autoclass:: FeaturesExtractorManager
    :members:

Informer
--------

.. autoclass:: Informer
    :members:

.. autoclass:: Colors
    :members:

Multiprocess
------------

.. autoclass:: MultiprocessManager
    :members:

Storage
-------

.. autoclass:: FeaturesSaver
    :members:

.. autoclass:: PipelineFeaturesFormatLoader
    :members:

