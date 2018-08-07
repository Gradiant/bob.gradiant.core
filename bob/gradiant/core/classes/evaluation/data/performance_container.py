#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain


class PerformanceContainer:
    def __init__(self, performance, type_eval, fps, t_capture, attack_type, name_dataset, name_algorithm):
        self.performance = performance
        self.type = type_eval
        self.fps = fps
        self.t_capture = t_capture
        self.attack = attack_type
        self.dataset = name_dataset
        self.algorithm = name_algorithm