#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import warnings
import numpy
import os

from bob.gradiant.core.classes.evaluation.utils.hdf5_utils import save_dict_to_hdf5, load_dict_from_hdf5, convert_from_unicode_string

class ExperimentResult(object):

    @staticmethod
    def load(path_filename):

        dict_from_file = load_dict_from_hdf5(path_filename)

        attacks_correspondences = convert_from_unicode_string(dict_from_file['attacks_correspondences'])

        experiment_result = ExperimentResult(str(dict_from_file['name_algorithm']),
                                             str(dict_from_file['pipeline_description']),
                                             str(dict_from_file['name_dataset']),
                                             dict_from_file['scores'],
                                             dict_from_file['labels'],
                                             int(dict_from_file['framerate']),
                                             int(dict_from_file['time_capture']),
                                             bool(dict_from_file['is_distance']),
                                             attacks_correspondences)
        return experiment_result


    def __init__(self, name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences):
        self.assert_inputs(name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences)
        self.name_algorithm = name_algorithm
        self.pipeline_description = pipeline_description
        self.name_dataset = name_dataset
        self.scores = scores
        self.labels = labels
        self.framerate = framerate
        self.time_capture = time_capture
        self.is_distance = is_distance
        self.attacks_correspondences = attacks_correspondences

    def __str__(self):
        return '{} : {}'.format(self.__class__.__name__, dict(self))

    @classmethod
    def assert_inputs(cls, name_algorithm, pipeline_description, name_dataset, scores, labels, framerate, time_capture, is_distance, attacks_correspondences):
        if name_algorithm == '':
            raise ValueError("name_algorithm is empty")
        if name_dataset == '':
            raise ValueError("name_dataset is empty")
        if pipeline_description == '':
            raise ValueError("pipeline_description is empty")
        if not isinstance(scores, (numpy.ndarray, numpy.generic)):
            raise TypeError("scores must be a numpy array")
        if not isinstance(labels, (numpy.ndarray, numpy.generic)):
            raise TypeError("labels must be a numpy array")
        if framerate < 1:
            raise TypeError("framerate must be always positive")
        if time_capture < -1:
            raise TypeError("time_capture must be always positive (unless -1, which represents standard evaluation with whole video)")
        if (is_distance >= 2) or (is_distance < 0):
            raise TypeError("is_distance must be 0 or 1")
        if not attacks_correspondences:
            raise TypeError('attacks_correspondences is empty')

    def get_complete_title(self):
        # todo review
        complete_title = '_'.join(
            [self.name_algorithm, self.pipeline_description, self.name_dataset, str(self.framerate),
             str(self.time_capture)])
        return complete_title

    def __iter__(self):  # overridding this to return tuples of (key,value)
        return iter([('name_algorithm', self.name_algorithm),
                     ('pipeline_description', self.pipeline_description),
                     ('name_dataset', self.name_dataset),
                     ('scores', self.scores),
                     ('labels', self.labels),
                     ('framerate', self.framerate),
                     ('time_capture', self.time_capture),
                     ('is_distance',self.is_distance),
                     ('attacks_correspondences', self.attacks_correspondences)])

    def save(self, path_filename):
        dict_object = dict(self)
        if os.path.isfile(path_filename): warnings.warn('HDF5 file (' + path_filename + ') already exists, it will be overwritten.')
        save_dict_to_hdf5(dict_object, path_filename)
