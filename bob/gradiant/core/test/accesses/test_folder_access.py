#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
from mock import MagicMock, patch

from bob.gradiant.core import AccessModificator, FolderAccess
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestFolderAccess(unittest.TestCase):

    def test_constructor_with_wrong_base_path(self):
        base_path = ''
        name = 'access01'

        self.assertRaises(IOError,
                          lambda: FolderAccess(base_path,name)
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

    def test_constructor_with_wrong_access_modificator(self):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        access_modificator = None

        self.assertRaises(TypeError,
                          lambda: FolderAccess(base_path, name, access_modificator=access_modificator)
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
        dict_images = folder_access.load()

    dummy_dict_images = {'dummy', 'image'}
    @patch('bob.gradiant.core.classes.accesses.access_modificator.AccessModificator.run', MagicMock(return_value=dummy_dict_images))
    def test_constructor_with_valid_parameters_and_access_modificator(self, dummy_dict_images=dummy_dict_images):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        folder_access = FolderAccess(base_path, name,access_modificator=AccessModificator())
        dict_images = folder_access.load()
        AccessModificator.run.assert_called_once()

        self.assertEqual(dict_images, dummy_dict_images)

    dummy_dict_images = {'dummy', 'image'}
    @patch('bob.gradiant.core.classes.accesses.access_modificator.AccessModificator.run', MagicMock(return_value=dummy_dict_images))
    def test_constructor_with_valid_parameters_and_setter_access_modificator(self, dummy_dict_images=dummy_dict_images):
        base_path = TestUtils.get_resources_path()
        name = 'genuine'
        folder_access = FolderAccess(base_path, name)
        folder_access.set_access_modificator(AccessModificator())
        dict_images = folder_access.load()
        AccessModificator.run.assert_called_once()

        self.assertEqual(dict_images, dummy_dict_images)


