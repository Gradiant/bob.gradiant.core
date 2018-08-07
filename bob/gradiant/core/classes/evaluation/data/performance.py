#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain


class Performance:
    def __init__(self):
        self.values = {}

    def add(self, metric_name, value, threshold):
        self.values[metric_name] = [value, threshold]
