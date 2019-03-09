#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
from abc import ABCMeta, abstractmethod
from bob.gradiant.core.classes.accesses.access_modifier import AccessModifier
from enum import Enum


class TypeDatabase(Enum):
    SPLIT = 0
    ALL_FILES_TOGETHER = 1


class Database(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, base_path, type_database=TypeDatabase.SPLIT, annotation_base_path=None):
        if not os.path.isdir(base_path):
            raise IOError
        self.base_path = base_path
        self.type_database = type_database
        self.annotation_base_path = annotation_base_path

    @abstractmethod
    def __str__(self, name='Database'):
        return '{}: base_path : {} {}'.format(name, self.base_path, self.type_database)

    @abstractmethod
    def get_protocols(self):
        raise NotImplementedError

    @abstractmethod
    def get_subsets(self):
        raise NotImplementedError

    @abstractmethod
    def get_capture_devices(self):
        raise NotImplementedError

    @abstractmethod
    def get_attack_dict(self):
        raise NotImplementedError

    @abstractmethod
    def get_all_accesses(self, access_modifier=AccessModifier()):
        raise NotImplementedError

    @abstractmethod
    def get_all_labels(self, protocol):
        raise NotImplementedError

    @abstractmethod
    def get_ground_truth(self, protocol):
        raise NotImplementedError
