#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import AccessModificator
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestAccessModificator(unittest.TestCase):

    def test_constructor_with_empty_dict_images(self):

        dict_images = {}
        access_modificator = AccessModificator()
        self.assertRaises(ValueError,
                          lambda: access_modificator.run(dict_images)
                          )

    def test_constructor_with_none_dict_images(self):
        dict_images = None
        access_modificator = AccessModificator()

        self.assertRaises(ValueError,
                          lambda: access_modificator.run(dict_images)
                          )

    def test_constructor_with_correct_params_with_timestamp_reference_zero(self):
        dict_images = TestUtils.get_synthetic_dict_image( timestamp_reference= 0)
        access_modificator = AccessModificator()

        mod_dict_images = access_modificator.run(dict_images)

        self.assertEqual(dict_images, mod_dict_images)

    def test_constructor_with_correct_params(self):
        dict_images = TestUtils.get_synthetic_dict_image()
        access_modificator = AccessModificator()

        mod_dict_images = access_modificator.run(dict_images)

        self.assertNotEqual(dict_images, mod_dict_images)

    def test_str(self):
        access_modificator = AccessModificator()
        self.assertEqual(access_modificator.__str__(),'AccessModificator [ target_framerate = 30 | target_duration = -1 ]')
