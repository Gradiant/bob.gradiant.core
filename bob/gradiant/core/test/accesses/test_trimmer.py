#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import Trimmer
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestTrimmer(unittest.TestCase):

    def test_run_empty_dict_image(self):

        dict_images = {}

        self.assertRaises(ValueError,
                          lambda: Trimmer.run(dict_images)
                          )

    def test_run_none_dict_image(self):
        dict_images = None

        self.assertRaises(ValueError,
                          lambda: Trimmer.run(dict_images)
                          )

    def run_trimmer(self, target_duration):
        dict_image_reference = TestUtils.get_synthetic_dict_image( timestamp_reference= 0)
        dict_image = Trimmer.run(dict_image_reference, target_duration = target_duration)
        return dict_image, dict_image_reference

    def test_run_with_default_param(self):
        dict_image, dict_image_reference = self.run_trimmer(-1)

        self.assertEqual(len(dict_image_reference), len(dict_image))

    def test_run_with_1000_ms(self):
        dict_image, dict_image_reference = self.run_trimmer(1000)

        self.assertEqual(len(dict_image_reference)/5 + 1, len(dict_image))

    def test_run_with_2500_ms(self):
        dict_image, dict_image_reference = self.run_trimmer(2500)

        self.assertEqual(len(dict_image_reference) / 2, len(dict_image))

    def test_run_with_more_target_duration_than_total_video(self):
        self.assertRaises(IndexError,
                                lambda: self.run_trimmer(5000)
                         )