#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import numpy as np

from bob.gradiant.core import ScoresContainer

class UnitTestPadInfo(unittest.TestCase):

    scores = np.array((0.5, 0.6, 0.5, 0.0, 0.1, 0.2, 0.3, 0.3, 0.3))
    labels = np.array((0,0,0,1,1,1,2,2,2))

    def test_constructor(self):
        scores_container = ScoresContainer(self.scores, self.labels)

        np.testing.assert_array_equal(scores_container.scores,self.scores)
        np.testing.assert_array_equal(scores_container.labels,self.labels)

    def test_get_scores_and_labels(self):
        benchmark_scores = np.array((0.5, 0.6, 0.5, 0.0, 0.1, 0.2, 0.3, 0.3, 0.3))
        benchmark_labels = np.array((0,0,0,1,1,1,2,2,2))

        scores_container = ScoresContainer(self.scores, self.labels)

        scores, labels = scores_container.get_scores_and_labels()

        np.testing.assert_array_equal(scores,benchmark_scores)
        np.testing.assert_array_equal(labels, benchmark_labels)

    def test_print(self):
        scores_container = ScoresContainer(self.scores, self.labels)

        self.assertEqual(scores_container.__str__(),'ScoresContainer : scores [ 0.5  0.6  0.5  0.   0.1  0.2  0.3  0.3  0.3], labels [0 0 0 1 1 1 2 2 2]')



if __name__ == '__main__':
    unittest.main()