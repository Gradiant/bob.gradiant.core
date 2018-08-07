#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import TimestampNormalizer
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestTimestampNormalizer(unittest.TestCase):

    def test_run_with_none_dict_images(self):
        dict_images = None

        self.assertRaises(ValueError,
                          lambda: TimestampNormalizer.run(dict_images)
                          )

    def test_run_with_empty_dict_images(self):
        dict_images = {}

        self.assertRaises(ValueError,
                          lambda: TimestampNormalizer.run(dict_images)
                          )

    def test_run_with_syntetic_data_start_on_1500000000(self):
        dict_images = TestUtils.get_synthetic_dict_image()

        normalized_dict_images = TimestampNormalizer.run(dict_images)

        reference_list_keys = [x - 1500000000 for x in sorted(dict_images.keys())]
        self.assertEqual(reference_list_keys,sorted(normalized_dict_images.keys()))

    def test_run_with_syntetic_data_start_on_0(self):
        timestamp_reference = 0
        dict_images = TestUtils.get_synthetic_dict_image( timestamp_reference= timestamp_reference)

        normalized_dict_images = TimestampNormalizer.run(dict_images)

        reference_list_keys = [x - timestamp_reference for x in sorted(dict_images.keys())]
        self.assertEqual(reference_list_keys,sorted(normalized_dict_images.keys()))




