#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
from bob.gradiant.core import EndToEndInfo
import numpy as np
import os

from bob.gradiant.core.test.test_utils import TestUtils


class UnitTestEndToEndInfo(unittest.TestCase):

    name_algorithm = 'name_algorithm'
    framerate = 15
    total_time_of_acquisition = 500
    processor = 'Intel(R) Xeon(R) CPU X5675 @ 3.07GHz'
    processed_frames = 5
    scores_list = list(np.arange(0,1,0.2))
    time_of_delay_list = [0.15, 0.2, 0.25, 0.30, 0.35]
    cpu_time_list = [0.1, 0.15, 0.20, 0.25, 0.30]
    labels_list = ['ATTACK', 'ATTACK', 'ATTACK', 'NO ATTACK', 'NO ATTACK']
    benchmark_labels_list = ['ATTACK', 'ATTACK', 'NO ATTACK', 'NO ATTACK', 'NO ATTACK']

    def setUp(self):
        self.result_path = os.path.join(TestUtils.get_result_path(), 'end_to_end_info.h5')

    def tearDown(self):
        if os.path.isfile(self.result_path):
            os.remove(self.result_path)

    def test_constructor_with_correct_params(self):
        end_to_end_info = EndToEndInfo(self.name_algorithm,
                                       self.framerate,
                                       self.total_time_of_acquisition,
                                       self.processor,
                                       self.processed_frames,
                                       self.scores_list,
                                       self.time_of_delay_list,
                                       self.cpu_time_list,
                                       self.labels_list,
                                       self.benchmark_labels_list)

        self.assertTrue(isinstance(end_to_end_info,EndToEndInfo))

    def test_save(self):
        end_to_end_info = EndToEndInfo(self.name_algorithm,
                                       self.framerate,
                                       self.total_time_of_acquisition,
                                       self.processor,
                                       self.processed_frames,
                                       self.scores_list,
                                       self.time_of_delay_list,
                                       self.cpu_time_list,
                                       self.labels_list,
                                       self.benchmark_labels_list)
        end_to_end_info.save(self.result_path)

        self.assertTrue(os.path.isfile(self.result_path))

    def test_save_and_load_from_filename(self):
        end_to_end_info = EndToEndInfo(self.name_algorithm,
                                       self.framerate,
                                       self.total_time_of_acquisition,
                                       self.processor,
                                       self.processed_frames,
                                       self.scores_list,
                                       self.time_of_delay_list,
                                       self.cpu_time_list,
                                       self.labels_list,
                                       self.benchmark_labels_list)
        end_to_end_info.save(self.result_path)

        end_to_end_info_fromfile = EndToEndInfo.fromfilename(self.result_path)

        self.assert_end_to_end_info_equal(end_to_end_info, end_to_end_info_fromfile)

    def assert_end_to_end_info_equal(self, end_to_end_info, end_to_end_info_fromfile):
        self.assertEqual(end_to_end_info.name_algorithm, end_to_end_info_fromfile.name_algorithm)
        self.assertEqual(end_to_end_info.framerate, end_to_end_info_fromfile.framerate)
        self.assertEqual(end_to_end_info.total_time_of_acquisition, end_to_end_info_fromfile.total_time_of_acquisition)
        self.assertEqual(end_to_end_info.processor, end_to_end_info_fromfile.processor)
        self.assertEqual(end_to_end_info.processed_frames, end_to_end_info_fromfile.processed_frames)
        self.assertAlmostEqual(end_to_end_info.scores_list, end_to_end_info_fromfile.scores_list)
        self.assertAlmostEqual(end_to_end_info.time_of_delay_list, end_to_end_info_fromfile.time_of_delay_list)
        self.assertAlmostEqual(end_to_end_info.cpu_time_list, end_to_end_info_fromfile.cpu_time_list)
        self.assertAlmostEqual(end_to_end_info.labels_list, end_to_end_info_fromfile.labels_list)
        self.assertAlmostEqual(end_to_end_info.benchmark_labels_list, end_to_end_info_fromfile.benchmark_labels_list)





