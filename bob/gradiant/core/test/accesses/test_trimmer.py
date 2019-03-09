#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from __future__ import division
import unittest

from bob.gradiant.core import Trimmer
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestTrimmer(unittest.TestCase):

    def test_should_throw_an_exception_is_run_with_empty_dict_image(self):
        dict_images = {}
        self.assertRaises(ValueError,
                          lambda: Trimmer.run(dict_images)
                          )

    def test_should_throw_an_exception_is_run_with_none_dict_image(self):
        dict_images = None
        self.assertRaises(ValueError,
                          lambda: Trimmer.run(dict_images)
                          )

    def test_should_throw_an_exception_when_is_run_with_more_target_duration_than_total_video(self):
        dict_image_reference = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        not_valid_target_duration = 5000
        self.assertRaises(IndexError,
                          lambda: Trimmer.run(dict_image_reference, target_duration=not_valid_target_duration)
                          )

    def test_should_throw_an_exception_when_is_run_with_more_starting_time_than_total_video(self):
        dict_image_reference = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        not_valid_starting_time = 5000
        self.assertRaises(IndexError,
                          lambda: Trimmer.run(dict_image_reference, starting_time=not_valid_starting_time)
                          )

    def test_should_return_same_len_dict_when_is_run_with_default_param(self):
        dict_image_reference = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        dict_image = Trimmer.run(dict_image_reference)
        self.assertEqual(len(dict_image_reference), len(dict_image))

    def test_should_return_a_smaller_version_when_is_run_with_target_duration_1000_ms(self):
        dict_image_reference = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        dict_image = Trimmer.run(dict_image_reference, target_duration=1000)

        self.assertEqual(len(dict_image_reference) // 5 + 1, len(dict_image))

    def test_should_return_a_smaller_version_when_is_run_with_target_duration_2500_ms(self):
        dict_image_reference = TestUtils.get_synthetic_dict_image(timestamp_reference=0)

        dict_image = Trimmer.run(dict_image_reference, target_duration=2500)

        self.assertEqual(len(dict_image_reference) // 2, len(dict_image))

    def test_should_return_a_smaller_version_when_is_run_with_target_duration_1000_ms_and_starting_time_1000ms(self):
        dict_image_reference = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        dict_image = Trimmer.run(dict_image_reference, target_duration=1000, starting_time=1000)

        self.assertEqual(len(dict_image_reference) // 5 + 1, len(dict_image))

    def test_should_return_a_smaller_version_cropped_by_the_center_when_is_run_with_target_duration_1000_ms_and_center_video_acquisition(self):
        dict_image_reference = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        dict_image = Trimmer.run(dict_image_reference, target_duration=1000, center_video_acquisition=True)

        self.assertEqual(len(dict_image_reference) // 5, len(dict_image))


