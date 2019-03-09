#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import numpy as np
import h5py
import os
import unittest
import shutil
from bob.gradiant.core import FeaturesSaver
from bob.gradiant.core.test.test_utils import TestUtils


class TestFeaturesSaver(unittest.TestCase):
    result_path = TestUtils.get_result_path()

    def setUp(self):
        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

    def tearDown(self):
        if os.path.isdir(self.result_path):
            shutil.rmtree(self.result_path)

    def test_entry_dictionary_is_empty(self):
        empty_dict = {}
        features_saver = FeaturesSaver()
        self.assertRaises(TypeError,
                          lambda: features_saver.save(self.result_path, 'basename', empty_dict)
                          )

    def test_entry_dictionary_is_none(self):
        empty_dict = None
        features_saver = FeaturesSaver()
        self.assertRaises(TypeError,
                          lambda: features_saver.save(self.result_path, 'basename', empty_dict)
                          )

    def test_hdf5_file_already_exists(self):
        dict_features = {'grad000_real_00_00': np.array([1, 2, 3])}

        features_saver = FeaturesSaver()
        features_saver.set_base_path(self.result_path)
        features_saver.save('basename', dict_features)
        self.assertTrue(features_saver.file_exists('basename'))

    def test_hdf5_file_no_exists(self):
        features_saver = FeaturesSaver()
        features_saver.set_base_path(self.result_path)

        self.assertFalse(features_saver.file_exists('wrong_name'))

    def test_save_with_row_features(self):
        dict_features = {'grad000_real_00_00': np.array([1, 2, 3]),
                         'grad000_real_00_01': np.array([1, 2, 3])}
        keyframe_array = np.array(['grad000_real_00_00', 'grad000_real_00_01'])
        features_array = np.array([[1, 2, 3], [1, 2, 3]])

        features_saver = FeaturesSaver()
        features_saver.set_base_path(self.result_path)
        features_saver.save('basename', dict_features)
        filename = os.path.join(TestUtils.get_result_path(), 'basename.h5')
        file_root = h5py.File(filename, 'r')
        keyframe = file_root['/keyframe'][...]
        keyframe = [x.decode('utf-8') for x in keyframe]
        features = file_root['/features'][...]

        self.assertTrue(np.array_equal(keyframe, keyframe_array))
        self.assertTrue(np.array_equal(features, features_array))


if __name__ == '__main__':
    unittest.main()
