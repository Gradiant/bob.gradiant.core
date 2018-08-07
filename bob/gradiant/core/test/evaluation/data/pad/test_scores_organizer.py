#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import os
from bob.gradiant.core import ExperimentResultLoader, ScoresOrganizer
from bob.gradiant.core.test.test_utils import TestUtils
from sklearn.model_selection import ParameterGrid

class UnitTestScoresOrganizer(unittest.TestCase):

    parameters_grid = list(ParameterGrid({'type_attacks': ['all_attacks', 'print', 'replay'], 'framerate': [10, 15, 20], 'time_capture': [1000, 2000, -1]}))

    def test_run_with_correct_parameters(self):
        folder = os.path.join(TestUtils.get_resources_path(),'evaluation/experiment_result_files')
        list_experiment_result = ExperimentResultLoader.load_from_folder(folder)

        subset_data = ScoresOrganizer.run(list_experiment_result)

        self.assertEqual(len(subset_data.parameters_grid), len(self.parameters_grid))
        self.assertEqual(len(subset_data.list_pad_data), len(self.parameters_grid))


    def test_run_with_null_list_experiment_result(self):
        self.assertRaises(TypeError,
                          lambda : ScoresOrganizer.run(None)
                          )

if __name__ == '__main__':
    unittest.main()