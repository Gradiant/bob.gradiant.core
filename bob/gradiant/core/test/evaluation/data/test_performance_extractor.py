#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

import numpy as np
from bob.gradiant.core import ExperimentResultLoader, ScoresContainer, ScoresOrganizer, PerformanceExtractor, Metric
from bob.gradiant.core.test.test_utils import TestUtils

class MockMetric(Metric):
    def __init__(self, name):
        super(MockMetric, self).__init__(name, 'MockMetric')

    def compute(self, y_score, y_true):
        pass

class UnitTestPerformanceExtractor(unittest.TestCase):

    dict_subset_data = {}
    for subset in ['Dev', 'Test']:
        experiment_result_path = TestUtils.get_resources_path() + '/evaluation/subsets/' + subset.lower()
        list_experiment_result = ExperimentResultLoader.load_from_folder(experiment_result_path)
        subset_data = ScoresOrganizer.run(list_experiment_result)
        dict_subset_data[subset] = subset_data

    scores = np.array((0.9, 0.6, 0.8, 0.2, 0.3, 0.5))
    labels = np.array((0, 0, 0, 1, 1, 2))

    def test_eer(self):
        metrics = 'EER'
        scores_container = ScoresContainer(self.scores, self.labels)

        performance = PerformanceExtractor.run(metrics, scores_container)

        self.assertEquals({'threshold': 0.55, 'value': 0.0}, performance)

    def test_data_error(self):
        metrics = 'EER'
        scores_container = ScoresContainer(np.array([]), np.array([]))

        self.assertRaises(TypeError,
                          lambda: PerformanceExtractor.run(metrics, scores_container)
                          )


