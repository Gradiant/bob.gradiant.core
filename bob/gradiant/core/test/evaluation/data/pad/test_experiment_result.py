#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import shutil
import unittest

import numpy

from bob.gradiant.core import ExperimentResult
from bob.gradiant.core.test.test_utils import TestUtils

class UnitTestExperimentResult(unittest.TestCase):

    def test_correct_parameters_and_get_complete_name(self):
        experiment_result = self.get_experiment_result_valid_object()

        self.assertEqual(experiment_result.get_complete_title(), 'algorithm_pca95_lsvc_database_30_2000')

    def test_wrong_parameter_name_algorithm(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        name_algorithm = ''

        self.assertRaises(ValueError,
                          lambda: ExperimentResult(name_algorithm,
                                                 pipeline_description,
                                                 name_dataset,
                                                 scores,
                                                 labels,
                                                 framerate,
                                                 time_capture,
                                                 is_distance,
                                                 attacks_correspondences)
                          )

    def test_wrong_parameter_pipeline_description(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        pipeline_description = ''

        self.assertRaises(ValueError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

    def test_wrong_parameter_name_dataset(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        name_dataset = ''

        self.assertRaises(ValueError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

    def test_wrong_parameter_scores(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        scores = None

        self.assertRaises(TypeError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

    def test_wrong_parameter_labels(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        labels = None

        self.assertRaises(TypeError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

    def test_wrong_parameter_framerate(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        framerate = 0

        self.assertRaises(TypeError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

    def test_wrong_parameter_time_capture(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        time_capture = -2

        self.assertRaises(TypeError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

    def test_wrong_parameter_is_distance(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        is_distance = -1

        self.assertRaises(TypeError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

        is_distance = 3
        self.assertRaises(TypeError,
                          lambda: ExperimentResult(name_algorithm,
                                                   pipeline_description,
                                                   name_dataset,
                                                   scores,
                                                   labels,
                                                   framerate,
                                                   time_capture,
                                                   is_distance,
                                                   attacks_correspondences)
                          )

    def test_initialize_dict_from_experiment_result_object(self):
        experiment_result = self.get_experiment_result_valid_object()
        dict_experiment_result = dict(experiment_result)

        self.assertEqual(dict_experiment_result['name_algorithm'], 'algorithm')
        self.assertEqual(dict_experiment_result['name_dataset'], 'database')

    def test_save_and_load_object(self):
        path_filename = os.path.join(TestUtils.get_result_path(),'experiment_result.h5')
        experiment_result = self.get_experiment_result_valid_object()

        if not os.path.isdir(TestUtils.get_result_path()):
            os.mkdir(TestUtils.get_result_path())

        experiment_result.save(path_filename)
        experiment_result_red = ExperimentResult.load(path_filename)

        self.assertEqual(experiment_result_red.get_complete_title(),experiment_result.get_complete_title())

        if not os.path.isdir(TestUtils.get_result_path()):
            shutil.rmtree(TestUtils.get_result_path())

    def test_constructor_with_wrong_path(self):

        self.assertRaises(IOError,
                           lambda: ExperimentResult.load('wrong_path')
                          )

    def get_experiment_result_valid_object(self):
        name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences = self.get_correct_parameters()
        experiment_result = ExperimentResult(name_algorithm,
                                             pipeline_description,
                                             name_dataset,
                                             scores,
                                             labels,
                                             framerate,
                                             time_capture,
                                             is_distance,
                                             attacks_correspondences)
        return experiment_result

    def get_correct_parameters(self):
        name_algorithm = 'algorithm'
        pipeline_description = 'pca95_lsvc'
        name_dataset = 'database'
        scores = numpy.array((0.5, 0.6, 0.2, 0.1))
        labels = numpy.array((1, 1, 0, 0))
        framerate = 30
        time_capture = 2000
        is_distance = True
        attacks_correspondences = { 'print' : 1,
                                    'replay' : 2}
        return name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences


if __name__ == '__main__':
    unittest.main()