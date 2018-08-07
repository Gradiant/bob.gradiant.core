#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import bob.measure
from bob.gradiant.core.classes.evaluation.metrics.metric import Metric


class Hter(Metric):
    def __init__(self, name, threshold=None):
        super(Hter, self).__init__(name, 'HTER')
        self.threshold = threshold
        self.threshold_needed = True

    def compute(self, y_score, y_true):

        genuine_score = y_score[y_true == 0]
        impostor_score = y_score[y_true > 0]

        far, frr = bob.measure.farfrr(impostor_score, genuine_score, self.threshold)
        hter = (far + frr) / 2
        return 100*hter, self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold

