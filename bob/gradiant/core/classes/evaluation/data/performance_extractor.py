#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.evaluation.metrics.metric_provider import metric_provider


class PerformanceExtractor:

    @staticmethod
    def run(metric, scores_container, threshold=None):

        scores, labels = scores_container.get_scores_and_labels()

        PerformanceExtractor.__assert_input(labels, scores)

        try:
            metric_object = metric_provider[metric]
            if threshold is not None:
                metric_object.set_threshold(threshold)
            elif metric_object.metric_needs_threshold():
                raise Exception("Metric " + metric + " needs a threshold value but None has been provided.")
            value, threshold = metric_object.compute(scores, labels)
            return {'value': value, 'threshold': threshold}
        except:
            pass

    @staticmethod
    def __assert_input(labels, scores):
        if not scores.size:
            raise TypeError('Scores are empty')
        if not labels.size:
            raise TypeError('Labels are empty')
