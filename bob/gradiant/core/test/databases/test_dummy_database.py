#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import DummyDatabase
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestDummyDatabase(unittest.TestCase):

    def test_constructor_with_non_existing_path(self):
        self.assertRaises(IOError,
                          lambda: DummyDatabase('wrong_path')
                          )

    def test_name_static_method(self):
        self.assertEqual(DummyDatabase.name(), 'dummy-database')

    def test_is_a_collection_of_databases_static_method(self):
        self.assertFalse(DummyDatabase.is_a_collection_of_databases())

    def test_constructor_with_correct_path_and_get_all_accesses(self):

        dummy_database = DummyDatabase(TestUtils.get_resources_path())
        list_accesses = dummy_database.get_all_accesses()

        self.assertEquals(len(list_accesses), 2)

    def test_constructor_with_correct_path_and_get_labeled_dict_from_list_basename(self):
        dummy_database = DummyDatabase(TestUtils.get_resources_path())

        dict_labels = dummy_database.get_ground_truth('Protocol_1')

        for subset in dummy_database.get_subsets():
            self.assertEquals(dict_labels[subset]['genuine'], 0)
            self.assertEquals(dict_labels[subset]['impostor'], 1)

