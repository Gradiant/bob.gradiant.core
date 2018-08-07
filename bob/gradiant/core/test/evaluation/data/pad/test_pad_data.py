#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np

from bob.gradiant.core import PadData, PadInfo, ScoresContainer

class UnitTestPadData(unittest.TestCase):

    pad_info = PadInfo('all_attacks',15, 1000)
    scores_container = ScoresContainer(np.array((0.5, 0.6, 0.5, 0.0, 0.1, 0.2)),
                                       np.array((0, 0, 0, 1, 1, 1)))

    def test_constructor(self):

        pad_data = PadData(self.pad_info, self.scores_container)

        self.assertEqual(pad_data.pad_info, self.pad_info)
        self.assertEqual(pad_data.scores_container, self.scores_container)

    def test_print(self):
        pad_data = PadData(self.pad_info, self.scores_container)
        self.assertEqual(pad_data.__str__(),'PadData : PadInfo : type_attacks : all_attacks, framerate : 15, time_capture : 1000 , ScoresContainer : scores [ 0.5  0.6  0.5  0.   0.1  0.2], labels [0 0 0 1 1 1]')

    def test_empty_pad_info(self):
        self.assertRaises(TypeError,
                          lambda: PadData(None, self.scores_container)
                          )

    def test_empty_scores_container(self):
        self.assertRaises(TypeError,
                          lambda: PadData(self.pad_info, None)
                          )

if __name__ == '__main__':
    unittest.main()