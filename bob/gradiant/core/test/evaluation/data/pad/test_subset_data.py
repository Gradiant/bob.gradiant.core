#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np

from bob.gradiant.core import PadData, PadInfo, ScoresContainer, SubsetData
from sklearn.model_selection import ParameterGrid

class UnitSubsetData(unittest.TestCase):

    pad_info = PadInfo('all_attacks',15, 1000)
    scores_container = ScoresContainer(np.array((0.5, 0.6, 0.5)),  # genuine
                                       np.array((0.0, 0.1, 0.2)))  # impostor
    pad_data = PadData(pad_info, scores_container)

    parameters_grid = list(ParameterGrid({'attack': ['all_attacks', ['print'], ['replay']], 'framerate': [10, 15, 20], 'time_capture': [1000, 2000]}))
    list_pad_data = [pad_data, pad_data]

    def test_constructor(self):

        subset_data = SubsetData(self.parameters_grid, self.list_pad_data)

        self.assertEqual(subset_data.parameters_grid, self.parameters_grid)
        self.assertEqual(subset_data.list_pad_data, self.list_pad_data)

    def test_print(self):
        subset_data = SubsetData(self.parameters_grid, self.list_pad_data)

        self.assertEqual(subset_data.__str__(),'SubsetData : len(parameters_grid) : 18 , len(list_pad_data) : 2')

    def test_empty_list_attacks(self):

        self.assertRaises(TypeError,
                            lambda:  SubsetData(None, self.list_pad_data)
                        )

    def test_empty_list_pad_data(self):
        self.assertRaises(TypeError,
                         lambda: SubsetData(self.parameters_grid, None)
                         )


if __name__ == '__main__':
    unittest.main()