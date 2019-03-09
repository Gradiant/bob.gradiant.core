#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from abc import ABCMeta, abstractmethod
from bob.gradiant.core.classes.accesses.access_modifier import AccessModifier


class Access(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 base_path,
                 name,
                 access_modifier=AccessModifier(),
                 annotation_base_path=None,
                 database_name=None):
        if not isinstance(access_modifier, AccessModifier):
            raise TypeError("input must be a AccessModifier")
        self.base_path = base_path
        self.name = name
        self.access_modifier = access_modifier
        self.annotation_base_path = annotation_base_path
        self.database_name = database_name

    @abstractmethod
    def load(self):
        raise NotImplementedError

    @abstractmethod
    def load_annotations(self):
        raise NotImplementedError
