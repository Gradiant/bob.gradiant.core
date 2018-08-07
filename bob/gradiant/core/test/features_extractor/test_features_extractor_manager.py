#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import shutil
import unittest

import h5py
import numpy
from mock import MagicMock, patch

from bob.gradiant.core import FeaturesExtractorManager, Informer, FeaturesSaver
from bob.gradiant.core.test.features_extractor.mock_access import MockAccess
from bob.gradiant.core.test.features_extractor.mock_features_extractor import MockFeaturesExtractor
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestFeaturesExtractorManager(unittest.TestCase):

    def setUp(self):
        self.dict_images = dict([('image_1', TestUtils.get_numpy_image())])
        self.features = numpy.array([0, 1, 2, 3])

        self.mock_features_extractor = MockFeaturesExtractor()
        self.mock_features_extractor.run = MagicMock(return_value=self.features)

        self.base_path = TestUtils.get_result_path()

        self.name_access = 'name_access'
        self.mock_access = MockAccess(TestUtils.get_resources_path(), self.name_access)
        self.mock_access.load = MagicMock(return_value=self.dict_images)

    def create_fake_h5_file(self):
        if not os.path.isdir(self.base_path):
            os.mkdir(self.base_path)
        filename_fake_h5 = os.path.join(self.base_path, self.name_access + '.h5')
        file_root = h5py.File(filename_fake_h5, 'w')
        file_root.close()

    def test_constructor_with_none_objects(self):
        features_extractor = None
        features_saver = None

        self.assertRaises(TypeError,
                          lambda: FeaturesExtractorManager(features_extractor, features_saver)
                          )

    @patch('bob.gradiant.core.classes.storage.features_saver.FeaturesSaver.save', MagicMock())
    # @patch('bob.gradiant.data.protocols.classes.informer.informer.Informer.message', MagicMock())
    def test_run_with_recreate_true(self):

        features_saver = FeaturesSaver(self.base_path)
        informer = Informer('access [1/100]')

        features_extractor_manager = FeaturesExtractorManager(self.mock_features_extractor, features_saver)
        features_extractor_manager.run(self.mock_access, informer=informer, recreate=True)

        self.mock_access.load.assert_called_once()
        self.mock_features_extractor.run.assert_called_once_with(self.dict_images, annotations = None)
        features_saver.save.assert_called_once()
        # informer.message.assert_called_once()

    @patch('bob.gradiant.core.classes.storage.features_saver.FeaturesSaver.save', MagicMock())
    # @patch('bob.gradiant.data.protocols.classes.informer.informer.Informer.message', MagicMock())
    def test_run_with_recreate_false_with_no_exists_file(self):

        features_saver = FeaturesSaver(self.base_path)
        informer = Informer('access [1/100]')

        features_extractor_manager = FeaturesExtractorManager(self.mock_features_extractor, features_saver)
        features_extractor_manager.run(self.mock_access, informer=informer, recreate=False)

        self.mock_access.load.assert_called_once()
        self.mock_features_extractor.run.assert_called_once_with(self.dict_images, annotations = None)
        FeaturesSaver.save.assert_called_once()
        # informer.message.assert_called_once()

    @patch('bob.gradiant.core.classes.storage.features_saver.FeaturesSaver.save', MagicMock())
    def test_run_with_recreate_false_with_exist_file(self):
        self.create_fake_h5_file()

        features_saver = FeaturesSaver(self.base_path)
        informer = Informer('access [1/100]')

        features_extractor_manager = FeaturesExtractorManager(self.mock_features_extractor, features_saver)
        features_extractor_manager.run(self.mock_access, informer=informer, recreate=False)

        self.mock_access.load.assert_not_called()
        self.mock_features_extractor.run.assert_not_called()
        features_saver.save.assert_not_called()
        informer = Informer('access [1/100]')

        if os.path.isdir(self.base_path):
            shutil.rmtree(self.base_path)








