#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.evaluation.data.pad.pad_info import PadInfo
from bob.gradiant.core.classes.evaluation.data.pad.scores_container import ScoresContainer

class PadData(object):
    def __init__(self, pad_info, scores_container):
        self.assert_input(pad_info, scores_container)
        self.pad_info = pad_info
        self.scores_container = scores_container

    @classmethod
    def assert_input(cls, pad_info, scores_container):
        if not isinstance(pad_info, PadInfo):
            raise TypeError('pad_info must be a PadInfo object')
        if not isinstance(scores_container, ScoresContainer):
            raise TypeError('scores_container must be a ScoresContainer object')


    def __str__(self):
        return '{} : {} , {}'.format(self.__class__.__name__,self.pad_info.__str__(), self.scores_container.__str__())