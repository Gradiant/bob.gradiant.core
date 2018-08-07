#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from abc import ABCMeta, abstractmethod


class Metric(object):
    __metaclass__ = ABCMeta
    name = None
    type = None
    threshold_needed = None

    def __init__(self, name, type):
        self.name = name
        self.type = type

    @staticmethod
    def assert_input(self, y_score, y_true):
        genuine_score = y_score[y_true == 0]
        impostor_score = y_score[y_true > 0]
        if not genuine_score.size or not impostor_score.size:
            raise TypeError("There is only one class. Impossible calculate a metric")

    @abstractmethod
    def compute(self, y_score, y_true):
        raise NotImplementedError

    def metric_needs_threshold(self):
        return self.threshold_needed
