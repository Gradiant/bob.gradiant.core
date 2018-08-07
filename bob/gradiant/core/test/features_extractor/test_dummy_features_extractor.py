#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import DummyFeaturesExtractor
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestDummyFeaturesExtractor(unittest.TestCase):

    def test_run_with_empty_input(self):
        dict_images = { 'image_1' : TestUtils.get_numpy_image()}
        dummy_features_extractor = DummyFeaturesExtractor()

        dict_features = dummy_features_extractor.run(dict_images)

        self.assertEqual(len(dict_images), len(dict_features))


