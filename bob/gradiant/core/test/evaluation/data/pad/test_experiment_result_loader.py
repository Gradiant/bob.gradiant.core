#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np
import os
from bob.gradiant.core import ExperimentResultLoader
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestExperimentResultLoader(unittest.TestCase):

    def test_run_with_correct_parameters(self):
        folder = os.path.join(TestUtils.get_resources_path(), 'evaluation/experiment_result_files')
        list_experiment_result = ExperimentResultLoader.load_from_folder(folder)
        self.assertEqual(len(list_experiment_result), 9)

    def test_run_with_wrong_path(self):
        folder = 'wrong_path'
        self.assertRaises(IOError,
                          lambda: ExperimentResultLoader.load_from_folder(folder)
                          )


if __name__ == '__main__':
    unittest.main()
