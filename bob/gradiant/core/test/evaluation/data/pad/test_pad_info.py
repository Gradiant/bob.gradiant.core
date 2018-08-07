#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import PadData, PadInfo

class UnitTestPadInfo(unittest.TestCase):
    type_attacks = 'all_attacks'
    framerate = 5
    time_capture = 1000

    def test_constructor(self):

        pad_info = PadInfo(self.type_attacks, self.framerate,self.time_capture)

        self.assertEqual(pad_info.type_attacks,self.type_attacks)
        self.assertEqual(pad_info.framerate,self.framerate)
        self.assertEqual(pad_info.time_capture,self.time_capture)

    def test_print(self):
        pad_info = PadInfo(self.type_attacks, self.framerate,self.time_capture)

        self.assertEqual(pad_info.__str__(),'PadInfo : type_attacks : all_attacks, framerate : 5, time_capture : 1000')


    def test_empty_type_attacks(self):

        self.assertRaises(TypeError,
                            lambda:  PadInfo(None, self.framerate, self.time_capture)
                        )

    def test_negative_framerate(self):

        self.assertRaises(TypeError,
                            lambda:  PadInfo(self.type_attacks, -1, self.time_capture)
                        )

    def test_standard_time_capture(self):
         pad_info = PadInfo(self.type_attacks, self.framerate, -1)
         self.assertNotEqual(pad_info, None)

    def test_negative_and_non_standard_time_capture(self):
        self.assertRaises(TypeError,
                          lambda: PadInfo(self.type_attacks, self.framerate, -2)
                          )

if __name__ == '__main__':
    unittest.main()