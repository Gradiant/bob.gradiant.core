#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
from mock import MagicMock, patch

from bob.gradiant.core import AccessModifier, FolderAccess
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestFolderAccess(unittest.TestCase):

    def test_constructor_with_wrong_base_path(self):
        base_path = ''
        name = 'access01'

        self.assertRaises(IOError,
                          lambda: FolderAccess(base_path, name)
                          )

    def test_constructor_with_wrong_name(self):
        base_path = TestUtils.get_resources_path()
        name = ''

        self.assertRaises(IOError,
                          lambda: FolderAccess(base_path, name)
                          )

    def test_constructor_with_wrong_base_path_and_name(self):
        base_path = TestUtils.get_resources_path()
        name = ''

        self.assertRaises(IOError,
                          lambda: FolderAccess(base_path, name)
                          )

    def test_constructor_with_wrong_access_modifier(self):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        access_modifier = None

        self.assertRaises(TypeError,
                          lambda: FolderAccess(base_path, name, access_modifier=access_modifier)
                          )

    def test_constructor_with_valid_parameters_but_pointing_no_images_folder(self):
        base_path = TestUtils.get_resources_path() + '/..'
        name = 'bob'
        folder_access = FolderAccess(base_path, name)

        self.assertRaises(IOError,
                          lambda: folder_access.load()
                          )

    def test_constructor_with_valid_parameters(self):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        folder_access = FolderAccess(base_path, name)
        _ = folder_access.load()

        self.assertTrue(isinstance(folder_access, FolderAccess))

    def test_constructor_with_valid_parameters_with_database_name(self):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        folder_access = FolderAccess(base_path, name, database_name='database_name')
        _ = folder_access.load()

        self.assertTrue(isinstance(folder_access, FolderAccess))
        self.assertEqual(folder_access.database_name, 'database_name')

    dummy_dict_images = {'dummy', 'image'}

    @patch('bob.gradiant.core.classes.accesses.access_modifier.AccessModifier.run', MagicMock(return_value=dummy_dict_images))
    def test_constructor_with_valid_parameters_and_access_modifier(self, dummy_dict_images=dummy_dict_images):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        folder_access = FolderAccess(base_path, name, access_modifier=AccessModifier())
        dict_images = folder_access.load()
        AccessModifier.run.assert_called_once()

        self.assertEqual(dict_images, dummy_dict_images)

    dummy_dict_images = {'dummy', 'image'}

    @patch('bob.gradiant.core.classes.accesses.access_modifier.AccessModifier.run', MagicMock(return_value=dummy_dict_images))
    def test_constructor_with_valid_parameters_and_setter_access_modifier(self, dummy_dict_images=dummy_dict_images):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        folder_access = FolderAccess(base_path, name)
        folder_access.set_access_modifier(AccessModifier())
        dict_images = folder_access.load()
        AccessModifier.run.assert_called_once()

        self.assertEqual(dict_images, dummy_dict_images)


