#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import warnings
import numpy as np

from bob.gradiant.core.classes.evaluation.utils.hdf5_utils import save_dict_to_hdf5, load_dict_from_hdf5, \
    convert_from_unicode_string

try:
    basestring
except NameError:
    basestring = str


class ExperimentResult(object):

    @staticmethod
    def load(path_filename):

        dict_from_file = load_dict_from_hdf5(path_filename)

        attacks_correspondences = convert_from_unicode_string(dict_from_file['attacks_correspondences'])
        devices_correspondences = convert_from_unicode_string(dict_from_file['devices_correspondences'])

        experiment_result = ExperimentResult(str(dict_from_file['name_algorithm']),
                                             str(dict_from_file['pipeline_description']),
                                             str(dict_from_file['name_dataset']),
                                             dict_from_file['scores'],
                                             dict_from_file['db_labels'],
                                             dict_from_file['common_pai'],
                                             dict_from_file['common_capture_devices'],
                                             int(dict_from_file['framerate']),
                                             int(dict_from_file['time_capture']),
                                             bool(dict_from_file['is_distance']),
                                             str(dict_from_file['access_names']),
                                             attacks_correspondences,
                                             devices_correspondences)
        return experiment_result

    def __init__(self, name_algorithm, pipeline_description, name_dataset, scores, db_labels, common_pai,
                 common_capture_devices, framerate, time_capture, is_distance, access_names, attacks_correspondences,
                 devices_correspondences):

        self.assert_inputs(name_algorithm, pipeline_description, name_dataset, scores, db_labels, common_pai,
                           common_capture_devices, framerate, time_capture, is_distance, access_names,
                           attacks_correspondences,
                           devices_correspondences)

        self.name_algorithm = name_algorithm
        self.pipeline_description = pipeline_description
        self.name_dataset = name_dataset
        self.scores = scores
        self.db_labels = db_labels
        self.common_pai = common_pai
        self.common_capture_devices = common_capture_devices
        self.framerate = framerate
        self.time_capture = time_capture
        self.is_distance = is_distance
        self.access_names = access_names
        self.attacks_correspondences = attacks_correspondences
        self.devices_correspondences = devices_correspondences

    def __str__(self):
        return '{} : {}'.format(self.__class__.__name__, dict(self))

    @classmethod
    def assert_inputs(cls, name_algorithm, pipeline_description, name_dataset, scores, db_labels, common_pai,
                      common_capture_devices, framerate, time_capture, is_distance, access_names,
                      attacks_correspondences,
                      devices_correspondences):

        if name_algorithm == '':
            raise ValueError("name_algorithm is empty")
        if name_dataset == '':
            raise ValueError("name_dataset is empty")
        if pipeline_description == '':
            raise ValueError("pipeline_description is empty")
        if not isinstance(scores, (np.ndarray, np.generic)):
            raise TypeError("scores must be a numpy array")
        if not isinstance(db_labels, (np.ndarray, np.generic)):
            raise TypeError("db_labels must be a numpy array")
        if not isinstance(common_pai, (np.ndarray, np.generic)):
            raise TypeError("common_pai must be a numpy array")
        if not isinstance(common_capture_devices, (np.ndarray, np.generic)):
            raise TypeError("common_capture_devices must be a numpy array")
        if framerate < 1:
            raise TypeError("framerate must be always positive")
        if time_capture < -1:
            raise TypeError(
                "time_capture must be always positive (unless -1, which represents standard evaluation with whole video)")
        if (is_distance >= 2) or (is_distance < 0):
            raise TypeError("is_distance must be 0 or 1")
        if not attacks_correspondences:
            raise TypeError('attacks_correspondences is empty')
        if not devices_correspondences:
            raise TypeError('devices_correspondences is empty')

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
                     ('db_labels', self.db_labels),
                     ('common_pai', self.common_pai),
                     ('common_capture_devices', self.common_capture_devices),
                     ('framerate', self.framerate),
                     ('time_capture', self.time_capture),
                     ('is_distance', self.is_distance),
                     ('access_names', self.access_names),
                     ('attacks_correspondences', self.attacks_correspondences),
                     ('devices_correspondences', self.devices_correspondences)])

    def save(self, path_filename):
        dict_object = dict(self)

        for key, value in dict_object.items():
            if self._is_list_of_strings(value):
                dict_object[key] = np.array(value, dtype='S')
            elif self._is_numpy_array_of_bytestrings(value):
                dict_object[key] = value.astype('S')
            else:
                continue

        if os.path.isfile(path_filename):
            warnings.warn('HDF5 file (' + path_filename + ') already exists, it will be overwritten.')
        save_dict_to_hdf5(dict_object, path_filename)

    @staticmethod
    def _is_list_of_strings(lst):
        if not isinstance(lst, list):
            return False
        else:
            return bool(lst) and not isinstance(lst, basestring) and all(isinstance(elem, basestring) for elem in lst)

    @staticmethod
    def _is_numpy_array_of_bytestrings(arr):
        if not isinstance(arr, np.ndarray):
            return False
        elif np.issubdtype(arr.dtype, np.str_):
            return True
        else:
            return False
