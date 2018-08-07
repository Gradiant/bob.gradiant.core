#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import bob.measure
from bob.gradiant.core.classes.evaluation.metrics.metric import Metric


class Eer(Metric):
    def __init__(self, name):
        super(Eer, self).__init__(name, 'EER')
        self.threshold_needed = False

    def compute(self, y_score, y_true):
        genuine_score = y_score[y_true == 0]
        impostor_score = y_score[y_true > 0]

        threshold_eer = bob.measure.eer_threshold(impostor_score, genuine_score)
        far, frr = bob.measure.farfrr(impostor_score, genuine_score, threshold_eer)
        eer = (far + frr) / 2
        return 100*eer, threshold_eer

    def set_threshold(self,threshold):
        pass
