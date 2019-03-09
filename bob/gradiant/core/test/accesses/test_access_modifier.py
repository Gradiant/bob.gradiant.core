#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import AccessModifier
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestAccessModifier(unittest.TestCase):

    def test_constructor_with_empty_dict_images(self):
        dict_images = {}
        access_modifier = AccessModifier()
        self.assertRaises(ValueError,
                          lambda: access_modifier.run(dict_images)
                          )

    def test_constructor_with_none_dict_images(self):
        dict_images = None
        access_modifier = AccessModifier()

        self.assertRaises(ValueError,
                          lambda: access_modifier.run(dict_images)
                          )

    def test_constructor_with_correct_params_with_timestamp_reference_zero(self):
        dict_images = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        access_modifier = AccessModifier()

        mod_dict_images = access_modifier.run(dict_images)

        self.assertEqual(dict_images, mod_dict_images)

    def test_should_return_an_access_normalized_when_run_with_default_params(self):
        dict_images = TestUtils.get_synthetic_dict_image()
        access_modifier = AccessModifier()

        mod_dict_images = access_modifier.run(dict_images)

        self.assertEqual(len(dict_images), len(mod_dict_images))
        self.assertNotEqual(dict_images, mod_dict_images)
        self.assertEqual(list(mod_dict_images)[0], 0)

    def test_should_return_an_access_normalized_and_trimmed_when_run_with_target_framerate_target_duration_and_starting_time(self):
        dict_images = TestUtils.get_synthetic_dict_image()
        access_modifier = AccessModifier(target_framerate=15, target_duration=1000, starting_time=100)

        mod_dict_images = access_modifier.run(dict_images)

        self.assertNotEqual(len(dict_images), len(mod_dict_images))
        self.assertEqual(len(mod_dict_images), 16)

    def test_should_return_an_access_normalized_and_trimmed_when_run_with_target_framerate_target_duration_and_center_video_acquisition(self):
        dict_images = TestUtils.get_synthetic_dict_image()
        access_modifier = AccessModifier(target_framerate=15, target_duration=1000, center_video_acquisition=True)

        mod_dict_images = access_modifier.run(dict_images)

        self.assertNotEqual(len(dict_images), len(mod_dict_images))
        self.assertEqual(len(mod_dict_images), 15)

    def test_str(self):
        access_modifier = AccessModifier()
        self.assertEqual(access_modifier.__str__(),
                         'AccessModifier [ target_framerate = 30 | '
                         'target_duration = -1 | '
                         'starting_time = -1 | '
                         'center_video_acquisition = False ]')
