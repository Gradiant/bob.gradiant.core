#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
from mock import MagicMock, patch
from bob.gradiant.core import AccessModifier, VideoAccess
from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestVideoAccess(unittest.TestCase):

    def test_constructor_with_wrong_base_path(self):
        base_path = ''
        name = 'access01'
        extension = '.mov'

        self.assertRaises(IOError,
                          lambda: VideoAccess(base_path, name, extension)
                          )

    def test_constructor_with_wrong_name(self):
        base_path = TestUtils.get_resources_path()
        name = ''
        extension = '.mov'

        self.assertRaises(IOError,
                          lambda: VideoAccess(base_path, name, extension)
                          )

    def test_constructor_with_wrong_base_path_and_name(self):
        base_path = TestUtils.get_resources_path()
        name = ''
        extension = '.avi'

        self.assertRaises(IOError,
                          lambda: VideoAccess(base_path, name, extension)
                          )

    def test_constructor_with_valid_parameters_but_pointing_no_video_folder(self):
        base_path = TestUtils.get_resources_path()
        name = 'video'
        extension = '.mov'
        access_modifier = None

        self.assertRaises(TypeError,
                          lambda: VideoAccess(base_path, name, extension, access_modifier)
                          )

    def test_constructor_with_valid_parameters_but_pointing_no_video_folder(self):
        base_path = TestUtils.get_resources_path() + '/..'
        name = 'bob'
        extension = '.mov'

        video_access = VideoAccess(base_path, name, extension)

        self.assertRaises(IOError,
                          lambda: video_access.load()
                          )

    def test_constructor_with_valid_parameters_pointing_a_image_instead_a_video(self):
        base_path = TestUtils.get_resources_path()
        name = 'todo_nexus'
        extension = '.mov'
        video_access = VideoAccess(base_path, name, extension)
        self.assertRaises(IOError,
                          lambda: video_access.load()
                          )

    def test_constructor_with_valid_parameters(self):
        base_path = TestUtils.get_resources_path()
        name = 'video'
        extension = '.mov'
        video_access = VideoAccess(base_path, name, extension)
        dict_images = video_access.load()
        self.assertEqual(len(dict_images), 6)
        self.assertTrue(isinstance(video_access, VideoAccess))

    def test_constructor_with_valid_parameters_with_database_name(self):
        base_path = TestUtils.get_resources_path()
        name = 'video'
        extension = '.mov'
        video_access = VideoAccess(base_path, name, extension, database_name='database_name')
        dict_images = video_access.load()
        self.assertEqual(len(dict_images), 6)
        self.assertTrue(isinstance(video_access, VideoAccess))
        self.assertEqual(video_access.database_name, 'database_name')

    dummy_dict_images = {'dummy', 'image'}

    @patch('bob.gradiant.core.classes.accesses.access_modifier.AccessModifier.run',
           MagicMock(return_value=dummy_dict_images))
    def test_constructor_with_valid_parameters_and_access_modifier(self, dummy_dict_images=dummy_dict_images):
        base_path = TestUtils.get_resources_path()
        name = 'video'
        extension = '.mov'

        video_access = VideoAccess(base_path, name, extension, access_modifier=AccessModifier())
        dict_images = video_access.load()

        AccessModifier.run.assert_called_once()

        self.assertEqual(dict_images, dummy_dict_images)

    dummy_dict_images = {'dummy', 'image'}

    @patch('bob.gradiant.core.classes.accesses.access_modifier.AccessModifier.run',
           MagicMock(return_value=dummy_dict_images))
    def test_constructor_with_valid_parameters_with_setter_access_modifier(self,
                                                                              dummy_dict_images=dummy_dict_images):
        base_path = TestUtils.get_resources_path()
        name = 'video'
        extension = '.mov'

        video_access = VideoAccess(base_path, name, extension)
        video_access.set_access_modifier(AccessModifier())
        dict_images = video_access.load()

        AccessModifier.run.assert_called_once()

        self.assertEqual(dict_images, dummy_dict_images)
