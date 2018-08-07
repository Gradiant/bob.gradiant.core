#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import glob

from bob.gradiant.core.classes.accesses.access_modificator import AccessModificator
from bob.gradiant.core.classes.accesses.folder_access import FolderAccess
from bob.gradiant.core.classes.databases.database import Database

DUMMY_DATABASE_PROTOCOLS = ['Grandtest']
DUMMY_DATABASE_SUBSETS = ['Train', 'Dev', 'Test']
DUMMY_DATABASE_CONVENTION = { 'genuine' : '0',
                    'impostor' : '1'}

class DummyDatabase(Database):
    def __init__(self, base_path):
        super(DummyDatabase,self).__init__(base_path)

    def __str__(self):
        return super(DummyDatabase,self).__str__(name = self.__class__.__name__)

    @staticmethod
    def name():
        return 'dummy-database'

    @staticmethod
    def is_a_collection_of_databases():
        return False

    def get_all_accesses(self, access_modificator=AccessModificator()):
        access_genuine = FolderAccess(self.base_path, 'genuine', access_modificator=access_modificator)
        access_impostor = FolderAccess(self.base_path, 'impostor', access_modificator=access_modificator)
        return [access_genuine, access_impostor]

    def get_protocols(self):
        return DUMMY_DATABASE_PROTOCOLS

    def get_subsets(self):
        return DUMMY_DATABASE_SUBSETS

    def get_ground_truth(self, protocol):
        dict_labels = {}
        for subset in DUMMY_DATABASE_SUBSETS:
            dict_labels_subset = {}
            dict_labels_subset['genuine'] = '0'
            dict_labels_subset['impostor'] = '1'
            dict_labels[subset] = dict_labels_subset
        return dict_labels

    def get_attack_dict(self):
        attack_dict = [item for item in DUMMY_DATABASE_CONVENTION if item.value is not 0]
        return attack_dict