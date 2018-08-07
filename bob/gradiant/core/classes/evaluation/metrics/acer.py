#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.evaluation.metrics.apcer import Apcer
from bob.gradiant.core.classes.evaluation.metrics.bpcer import Bpcer
from bob.gradiant.core.classes.evaluation.metrics.metric import Metric


class Acer(Metric):
    def __init__(self, name, threshold=None):
        super(Acer, self).__init__(name, 'ACER')
        self.threshold = threshold
        self.threshold_needed = True

    def compute(self, y_score, y_true):
        apcer_object = Apcer('APCER', self.threshold)
        bpcer_object = Bpcer('BPCER', self.threshold)
        apcer_value, threshold_acer = apcer_object.compute(y_score, y_true)
        bpcer_value, threshold_bpcer = bpcer_object.compute(y_score, y_true)
        return (apcer_value + bpcer_value)/2.0, self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold