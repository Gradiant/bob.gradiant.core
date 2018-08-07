#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from abc import ABCMeta, abstractmethod
from bob.gradiant.core.classes.accesses.access_modificator import AccessModificator


class Access(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, base_path, name, access_modificator=AccessModificator(), annotation_base_path=None):
        if not isinstance(access_modificator, AccessModificator):
            raise TypeError("input must be a AccessModificator")
        self.base_path = base_path
        self.name = name
        self.access_modificator = access_modificator
        self.annotation_base_path = annotation_base_path

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def load_annotations(self):
        raise NotImplementedError
