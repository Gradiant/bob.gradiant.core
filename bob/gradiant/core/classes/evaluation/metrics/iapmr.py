#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import numpy as np
from bob.gradiant.core.classes.evaluation.metrics.metric import Metric

class Iapmr(Metric):
    """
    Impostor Attack Presentation Match Rate: In a full-system evaluation of a verification system, the proportion of
     impostor attack presentation accepted by the Face Recognition system as genuine presentations for each PAI species
    """
    def __init__(self, name, threshold=None):
        super(Iapmr, self).__init__(name, 'IAPMR')
        self.threshold = threshold
        self.threshold_needed = True

    def compute(self, y_score, y_true):
        attack_ids = np.unique(y_true)
        attack_ids = np.trim_zeros(attack_ids)  # Remove genuine labels
        result_attacks = {}
        for ind_attack in attack_ids:
            array_attacks = y_score[y_true == ind_attack]
            result = array_attacks[array_attacks >= self.threshold].shape[0] / float(len(array_attacks))
            result_attacks[ind_attack]=result
        return result_attacks, self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold