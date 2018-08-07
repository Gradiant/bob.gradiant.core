#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import bob.measure
from bob.gradiant.core.classes.evaluation.metrics.metric import Metric


class Far(Metric):
    def __init__(self, name, far_value):
        super(Far, self).__init__(name, 'FAR')
        self.FAR = far_value
        self.threshold_needed = False

    def compute(self, y_score, y_true):
        genuine_score = y_score[y_true == 0]
        impostor_score = y_score[y_true > 0]
        threshold_far = bob.measure.far_threshold(impostor_score, genuine_score, self.FAR)
        far, frr = bob.measure.farfrr(impostor_score, genuine_score, threshold_far)
        return 100*frr, threshold_far

    def set_threshold(self, threshold):
        pass
