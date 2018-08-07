#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import numpy as np

class ScoresContainer(object):

    def __init__(self, scores, labels):
        self.scores = scores
        self.labels = labels

    def get_scores_and_labels(self):
        return self.scores, self.labels

    def is_empty(self):
        empty = False
        number_labels = np.unique(self.labels)
        if self.scores.size == 0 or self.labels.size == 0 or number_labels.size < 2:
            empty = True
        return empty

    def __str__(self):
        return '{} : scores {}, labels {}'.format(self.__class__.__name__, self.scores, self.labels)