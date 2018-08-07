#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from sklearn.metrics import roc_auc_score
from bob.gradiant.core.classes.evaluation.metrics.metric import Metric


class Auc(Metric):

    def __init__(self, name):
        super(Auc, self).__init__(name, 'Auc')
        self.threshold_needed = False

    def compute(self, y_score, y_true):
        return roc_auc_score(y_true, y_score)

    def set_threshold(self, threshold):
        pass
