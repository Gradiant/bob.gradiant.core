#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

class SubsetData(object):
    def __init__(self, parameters_grid, list_pad_data):
        self.assert_input(parameters_grid, list_pad_data)
        self.parameters_grid = parameters_grid
        self.list_pad_data = list_pad_data

    @classmethod
    def assert_input(cls, parameters_grid, list_pad_data):
        if not parameters_grid:
            raise TypeError('parameters_grid is empty')
        if not list_pad_data:
            raise TypeError('list_pad_data is empty')

    def __str__(self):
        return '{} : len(parameters_grid) : {} , len(list_pad_data) : {}'.format(self.__class__.__name__,str(len(self.parameters_grid)), str(len(self.list_pad_data)))