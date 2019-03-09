#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from __future__ import division
import unittest

from bob.gradiant.core import FramerateModificator
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestFramerateModificator(unittest.TestCase):

    def test_run_with_empty_dict_images(self):
        dict_images = {}

        self.assertRaises(ValueError,
                          lambda: FramerateModificator.run(dict_images, target_framerate=0)
                          )

    def test_run_with_none_dict_images(self):
        dict_images = None

        self.assertRaises(ValueError,
                          lambda: FramerateModificator.run(dict_images, target_framerate=0)
                          )

    def test_run_with_negative_framerate(self):
        dict_images = TestUtils.get_synthetic_dict_image(timestamp_reference=0)

        self.assertRaises(IndexError,
                          lambda: FramerateModificator.run(dict_images, target_framerate=-1)
                          )

    def test_run_with_zero_framerate(self):
        dict_images = TestUtils.get_synthetic_dict_image(timestamp_reference=0)

        self.assertRaises(IndexError,
                          lambda: FramerateModificator.run(dict_images, target_framerate=0)
                          )

    def test_run_with_one_image_none(self):
        dict_images = TestUtils.get_synthetic_dict_image(timestamp_reference=0)
        dict_images[0] = None

        self.assertRaises(ValueError,
                          lambda: FramerateModificator.run(dict_images)
                          )

    def run_framerate_modificator(self, target_framerate):
        dict_image_reference = TestUtils.get_synthetic_dict_image()
        dict_image = FramerateModificator.run(dict_image_reference, target_framerate=target_framerate)
        return dict_image, dict_image_reference

    def test_run_with_30_fps(self):
        dict_image, dict_image_reference = self.run_framerate_modificator(30)

        self.assertEqual(len(dict_image_reference), len(dict_image))

    def test_run_with_15_fps(self):
        dict_image, dict_image_reference = self.run_framerate_modificator(15)

        self.assertEqual(len(dict_image_reference) // 2, len(dict_image))

    def test_run_with_10_fps(self):
        dict_image, dict_image_reference = self.run_framerate_modificator(10)

        self.assertEqual(len(dict_image_reference) // 3, len(dict_image))

    def test_run_with_1_fps(self):
        dict_image, dict_image_reference = self.run_framerate_modificator(1)

        self.assertEqual(5, len(dict_image))
