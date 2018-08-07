#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from bob.gradiant.core import MultiprocessManager, FeaturesExtractor
import unittest
from mock import MagicMock

class MockProcess(FeaturesExtractor):
    def __init__(self):
        super(MockProcess, self).__init__()

    def run(self, dict_images):
        pass

    def other_function(self,dict_images):
        pass


class DummyExtractor(FeaturesExtractor):
    def __init__(self):
        super(DummyExtractor, self).__init__()

    def run(self, dict_images):
        return dict_images

    def other_function(self,dict_images):
        return dict_images



class UnitTestProcessManager(unittest.TestCase):
    def setUp(self):

        self.mock_features_extractor = MockProcess()
        self.mock_features_extractor.run = MagicMock()
        self.mock_features_extractor.other_function = MagicMock()

    def test_default_run_process_manager_one_thread(self):
        multiprocess_manager = MultiprocessManager(1)

        multiprocess_manager.run(self.mock_features_extractor,[ (None,)])

        self.mock_features_extractor.run.assert_called_once()
        self.mock_features_extractor.other_function.assert_not_called()

    def test_other_function_process_manager_one_thread(self):
        multiprocess_manager = MultiprocessManager(1)

        multiprocess_manager.run(self.mock_features_extractor,[(None,)],'other_function')

        self.mock_features_extractor.run.assert_not_called()
        self.mock_features_extractor.other_function.assert_called_once()

    def test_proces_manager_multithread_ordered_result(self):
        args=[(1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,)]

        multiprocess_manager = MultiprocessManager(4)
        extractor = DummyExtractor()

        result = multiprocess_manager.run(extractor, args)
        self.assertEqual(len(result),len(args))

        for i in range(len(args)):
            self.assertEquals(args[i][0], result[i])
