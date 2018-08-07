#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from abc import ABCMeta, abstractmethod


class FeaturesExtractor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self, dict_images, annotations=None):
        raise NotImplementedError

    def __str__(self):
        return '{}'.format(self.__class__.__name__)


