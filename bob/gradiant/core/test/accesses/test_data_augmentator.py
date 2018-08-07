#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np
from bob.gradiant.core import DataAugmentator


class UnitTestDataAugmentator(unittest.TestCase):

    dict_images_original = {
        0: np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]]),
        1: np.array([[[11, 12], [13, 14]], [[15, 16], [17, 18]], [[19, 110], [111, 112]]]),
    }

    dict_images_mirror = {
        0: np.array([[[2, 1], [4, 3]], [[6, 5], [8, 7]], [[10, 9], [12, 11]]]),
        1: np.array([[[12, 11], [14, 13]], [[16, 15], [18, 17]], [[110, 19], [112, 111]]]),
    }

    dict_images_reverse = {
        0: np.array([[[11, 12], [13, 14]], [[15, 16], [17, 18]], [[19, 110], [111, 112]]]),
        1: np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]]),
    }

    dict_images_reverse_mirror = {
        0: np.array([[[12, 11], [14, 13]], [[16, 15], [18, 17]], [[110, 19], [112, 111]]]),
        1: np.array([[[2, 1], [4, 3]], [[6, 5], [8, 7]], [[10, 9], [12, 11]]]),
    }

    def test_data_augmentator_videos_when_false(self):
        data_augmentator = DataAugmentator(False)
        dict_images = data_augmentator.augment_sequences(self.dict_images_original)
        self.assertEqual(dict_images['original'], self.dict_images_original)
        self.assertEqual(len(dict_images), 1)

    def test_data_augmentator_videos_when_true(self):

        data_augmentator = DataAugmentator(True)
        dict_images = data_augmentator.augment_sequences(self.dict_images_original)

        self.assertEqual(dict_images['original'], self.dict_images_original)
        np.testing.assert_equal(dict_images['mirror'], self.dict_images_mirror)
        np.testing.assert_equal(dict_images['reverse'], self.dict_images_reverse)
        np.testing.assert_equal(dict_images['reverse-mirror'], self.dict_images_reverse_mirror)


