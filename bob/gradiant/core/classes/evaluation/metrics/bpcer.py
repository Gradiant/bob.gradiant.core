#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.evaluation.metrics.metric import Metric


class Bpcer(Metric):
    def __init__(self, name, threshold=None):
        super(Bpcer, self).__init__(name, 'BPCER')
        self.threshold = threshold
        self.threshold_needed = True

    def compute(self, y_score, y_true):
        genuine_score = y_score[y_true == 0]
        bpcer = genuine_score[genuine_score < self.threshold].shape[0]
        return 100*bpcer / float(len(genuine_score)), self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold