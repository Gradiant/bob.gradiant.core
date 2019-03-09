#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import unittest
import shutil
from bob.gradiant.core import PadEvaluator
from bob.gradiant.core import PadVisualizationManager
from bob.gradiant.core.test.test_utils import TestUtils

class IntegrationTestEvaluationAndVisualization(unittest.TestCase):

    def setUp(self):
        self.result_path = os.path.join(TestUtils.get_result_path(), 'integration')
        if os.path.isdir(self.result_path):
            shutil.rmtree(self.result_path)


    def test_integration(self):

        experiment_result_path_dev = TestUtils.get_resources_path() + '/evaluation/subsets/dev'
        experiment_result_path_test = TestUtils.get_resources_path() + '/evaluation/subsets/test'
        dict_paths = {'Dev': experiment_result_path_dev, 'Test': experiment_result_path_test}
        # We will calculate EER in the development subset and the HTER and BPCER using the EER threshold:
        dict_metrics = {'Dev': ['EER'],
                        'Test': ['EER', 'HTER@EER', 'ACER@EER', 'APCER@EER', 'BPCER@EER']}

        dict_performance_visualization = PadEvaluator.run(dict_paths, dict_metrics)

        name_database = "DATABASE_NAME"
        name_algorithm = "algorithm"
        date = "2017/09/08 - 16:26:15"

        visualization_manager = PadVisualizationManager(name_database, name_algorithm, date, dict_performance_visualization,
                                                     self.result_path)
        visualization_manager.plot_fig_pad_time()
        visualization_manager.plot_table()

    def test_integration_standard_evaluation(self):
        result_path = os.path.join(TestUtils.get_result_path(), 'integration_standard_evaluation')
        if not os.path.isdir(result_path):
            os.makedirs(result_path)

        experiment_result_path_dev = TestUtils.get_resources_path() + '/evaluation/subsets_only_standard_evaluation/dev'
        experiment_result_path_test = TestUtils.get_resources_path() + '/evaluation/subsets_only_standard_evaluation/test'
        dict_paths = {'Dev': experiment_result_path_dev, 'Test': experiment_result_path_test}
        # We will calculate EER in the development subset and the HTER and BPCER using the EER threshold:
        dict_metrics = {'Dev': ['EER'],
                        'Test': ['EER', 'HTER@EER', 'ACER@EER', 'APCER@EER', 'BPCER@EER']}

        dict_performance_visualization = PadEvaluator.run(dict_paths, dict_metrics)

        name_dataset = "OULU"
        name_algorithm = "stb"
        date = "2017/09/08 - 16:26:15"

        visualization_manager = PadVisualizationManager(name_dataset, name_algorithm, date,
                                                        dict_performance_visualization,
                                                        result_path)
        visualization_manager.plot_fig_pad_time()
        visualization_manager.plot_table()


if __name__ == '__main__':
    unittest.main()