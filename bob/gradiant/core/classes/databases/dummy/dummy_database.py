#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import glob

from bob.gradiant.core.classes.accesses.access_modifier import AccessModifier
from bob.gradiant.core.classes.accesses.folder_access import FolderAccess
from bob.gradiant.core.classes.databases.database import Database

DUMMY_DATABASE_PROTOCOLS = ['Grandtest']
DUMMY_DATABASE_SUBSETS = ['Train', 'Dev', 'Test']
DUMMY_DATABASE_CONVENTION = {'genuine': 0,
                             'impostor': 1}
DUMMY_DATABASE_DEVICES = {'device-1': 0,
                          'device-2': 1}


class DummyDatabase(Database):
    def __init__(self, base_path):
        super(DummyDatabase, self).__init__(base_path)

    def __str__(self):
        return super(DummyDatabase,self).__str__(name = self.__class__.__name__)

    @staticmethod
    def name():
        return 'dummy-database'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    @staticmethod
    def get_protocols():
        return DUMMY_DATABASE_PROTOCOLS

    @staticmethod
    def get_subsets():
        return DUMMY_DATABASE_SUBSETS

    @staticmethod
    def get_capture_devices():
        return DUMMY_DATABASE_DEVICES

    @staticmethod
    def get_attack_dict():
        attack_dict = [item for item in DUMMY_DATABASE_CONVENTION if item.value is not 0]
        return attack_dict

    def get_all_accesses(self, access_modifier=AccessModifier()):
        access_genuine = FolderAccess(self.base_path, 'genuine', access_modifier=access_modifier)
        access_impostor = FolderAccess(self.base_path, 'impostor', access_modifier=access_modifier)
        return [access_genuine, access_impostor]

    def get_all_labels(self):
        dict_labels = {}
        for subset in DUMMY_DATABASE_SUBSETS:
            dict_labels_subset = {'device_1': 0, 'device_2': 1}
            dict_labels[subset] = dict_labels_subset
        return dict_labels

    def get_ground_truth(self, protocol):
        dict_labels = {}
        self.get_all_labels
        for subset in DUMMY_DATABASE_SUBSETS:
            dict_labels_subset = {'genuine': 0, 'impostor': 1}
            dict_labels[subset] = dict_labels_subset
        return dict_labels
