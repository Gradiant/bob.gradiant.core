#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
from bob.gradiant.core import PadEvaluator
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestPadEvaluator(unittest.TestCase):

    benchmark_performance_visualization = {'Test': {'all_attacks': {'HTER@EER': {10: {1000: {'threshold': -0.25, 'value': 25.0}, 2000: {'threshold': -0.25, 'value': 25.0}, -1: {'threshold': -0.25, 'value': 25.0}}, 20: {1000: {'threshold': -0.25, 'value': 25.0}, 2000: {'threshold': -0.25, 'value': 25.0}, -1: {'threshold': -0.25, 'value': 25.0}}, 15: {1000: {'threshold': -0.25, 'value': 25.0}, 2000: {'threshold': -0.25, 'value': 25.0}, -1: {'threshold': -0.25, 'value': 25.0}}}, 'BPCER@EER': {10: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 20: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 15: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}}, 'EER': {10: {1000: {'threshold': -0.15000000000000002, 'value': 0.0}, 2000: {'threshold': -0.15000000000000002, 'value': 0.0}, -1: {'threshold': -0.15000000000000002, 'value': 0.0}}, 20: {1000: {'threshold': -0.15000000000000002, 'value': 0.0}, 2000: {'threshold': -0.15000000000000002, 'value': 0.0}, -1: {'threshold': -0.15000000000000002, 'value': 0.0}}, 15: {1000: {'threshold': -0.15000000000000002, 'value': 0.0}, 2000: {'threshold': -0.15000000000000002, 'value': 0.0}, -1: {'threshold': -0.15000000000000002, 'value': 0.0}}}}, 'print': {'HTER@EER': {10: {1000: {'threshold': -0.25, 'value': 50.0}, 2000: {'threshold': -0.25, 'value': 50.0}, -1: {'threshold': -0.25, 'value': 50.0}}, 20: {1000: {'threshold': -0.25, 'value': 50.0}, 2000: {'threshold': -0.25, 'value': 50.0}, -1: {'threshold': -0.25, 'value': 50.0}}, 15: {1000: {'threshold': -0.25, 'value': 50.0}, 2000: {'threshold': -0.25, 'value': 50.0}, -1: {'threshold': -0.25, 'value': 50.0}}}, 'BPCER@EER': {10: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 20: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 15: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}}, 'EER': {10: {1000: {'threshold': -0.15000000000000002, 'value': 0.0}, 2000: {'threshold': -0.15000000000000002, 'value': 0.0}, -1: {'threshold': -0.15000000000000002, 'value': 0.0}}, 20: {1000: {'threshold': -0.15000000000000002, 'value': 0.0}, 2000: {'threshold': -0.15000000000000002, 'value': 0.0}, -1: {'threshold': -0.15000000000000002, 'value': 0.0}}, 15: {1000: {'threshold': -0.15000000000000002, 'value': 0.0}, 2000: {'threshold': -0.15000000000000002, 'value': 0.0}, -1: {'threshold': -0.15000000000000002, 'value': 0.0}}}}, 'replay': {'HTER@EER': {10: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 20: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 15: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}}, 'BPCER@EER': {10: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 20: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 15: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}}, 'EER': {10: {1000: {'threshold': -0.3, 'value': 0.0}, 2000: {'threshold': -0.3, 'value': 0.0}, -1: {'threshold': -0.3, 'value': 0.0}}, 20: {1000: {'threshold': -0.3, 'value': 0.0}, 2000: {'threshold': -0.3, 'value': 0.0}, -1: {'threshold': -0.3, 'value': 0.0}}, 15: {1000: {'threshold': -0.3, 'value': 0.0}, 2000: {'threshold': -0.3, 'value': 0.0}, -1: {'threshold': -0.3, 'value': 0.0}}}}}, 'Dev': {'all_attacks': {'EER': {10: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 20: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 15: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}}}, 'print': {'EER': {10: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 20: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 15: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}}}, 'replay': {'EER': {10: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 20: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}, 15: {1000: {'threshold': -0.25, 'value': 0.0}, 2000: {'threshold': -0.25, 'value': 0.0}, -1: {'threshold': -0.25, 'value': 0.0}}}}}}

    def test_run_with_correct_parameters(self):
        experiment_result_path_dev = TestUtils.get_resources_path() + '/evaluation/subsets/dev'
        experiment_result_path_test = TestUtils.get_resources_path() + '/evaluation/subsets/test'
        dict_paths = {'Dev': experiment_result_path_dev, 'Test': experiment_result_path_test}
        # We will calculate EER in the development subset and the HTER and BPCER using the EER threshold:
        dict_metrics = {'Dev': ['EER'], 'Test': ['EER', 'HTER@EER', 'BPCER@EER']}
        dict_performance_visualization = PadEvaluator.run(dict_paths, dict_metrics)

        self.assertDictEqual(dict_performance_visualization, self.benchmark_performance_visualization)

    def test_run_with_wrong_threshold(self):
        experiment_result_path_dev = TestUtils.get_resources_path() + '/evaluation/subsets/dev'
        experiment_result_path_test = TestUtils.get_resources_path() + '/evaluation/subsets/test'
        dict_paths = {'Dev': experiment_result_path_dev, 'Test': experiment_result_path_test}
        # We will calculate EER in the development subset and the HTER and BPCER using the EER threshold:
        dict_metrics = {'Dev': ['EER'], 'Test': ['EER', 'HTER@FAR1', 'BPCER@EER']}
        self.assertRaises(TypeError, lambda: PadEvaluator.run(dict_paths, dict_metrics))


if __name__ == '__main__':
    unittest.main()
