#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from abc import ABCMeta, abstractmethod


class TableGenerator(object):
    __metaclass__ = ABCMeta
    name_database = None
    name_algorithm = None
    dict_performance = None
    result_path = None

    def __init__(self, name_database, name_algorithm, dict_performance, result_path):
        self.name_database = name_database
        self.name_algorithm = name_algorithm
        self.dict_performance = dict_performance
        self.result_path = result_path

    @abstractmethod
    def run(self):
        raise NotImplementedError
