#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import h5py
import warnings
import numpy as np

try:
    basestring
except NameError:
    basestring = str


class EndToEndInfo(object):
    @classmethod
    def fromfilename(cls, path_filename):
        if not os.path.isfile(path_filename):
            raise IOError('File (' + path_filename + ') does not exist')
        file_root = h5py.File(path_filename, 'r')
        dict_from_file = {}
        for key, value in file_root.items():
            dict_from_file[str(key)] = value[...]
        file_root.close()

        end_to_end_info = EndToEndInfo(str(dict_from_file['name_algorithm']),
                                       int(dict_from_file['framerate']),
                                       int(dict_from_file['total_time_of_acquisition']),
                                       str(dict_from_file['processor']),
                                       int(dict_from_file['processed_frames']),
                                       list(dict_from_file['scores_list']),
                                       list(dict_from_file['time_of_delay_list']),
                                       list(dict_from_file['cpu_time_list']),
                                       [x.decode('utf-8') for x in dict_from_file['labels_list']],
                                       [x.decode('utf-8') for x in dict_from_file['benchmark_labels_list']])

        return end_to_end_info

    def __init__(self, name_algorithm, framerate, total_time_of_acquisition, processor,
                 processed_frames, scores_list, time_of_delay_list, cpu_time_list, labels_list, benchmark_labels_list):

        self.assert_inputs(name_algorithm, framerate, total_time_of_acquisition, processor,
                           processed_frames, scores_list, time_of_delay_list, cpu_time_list, labels_list,
                           benchmark_labels_list)

        self.name_algorithm = name_algorithm
        self.framerate = framerate
        self.total_time_of_acquisition = total_time_of_acquisition
        self.processor = processor
        self.processed_frames = processed_frames
        self.scores_list = scores_list
        self.time_of_delay_list = time_of_delay_list
        self.cpu_time_list = cpu_time_list
        self.labels_list = labels_list
        self.benchmark_labels_list = benchmark_labels_list

    def __str__(self):
        return '{} : {}'.format(self.__class__.__name__, dict(self))

    @classmethod
    def assert_inputs(cls, name_algorithm, framerate, total_time_of_acquisition, processor,
                      processed_frames, scores_list, time_of_delay_list, cpu_time_list, labels_list,
                      benchmark_labels_list):

        if not isinstance(name_algorithm, basestring):
            raise ValueError("name_algorithm must be a basestring")
        if not isinstance(framerate, int):
            raise ValueError("framerate must be a int")
        if not isinstance(total_time_of_acquisition, int):
            raise ValueError("total_time_of_acquisition must be a int")
        if not isinstance(processor, basestring):
            raise ValueError("processor must be a basestring")
        if not isinstance(processed_frames, int):
            raise ValueError("processed_frames must be a int")
        if not isinstance(scores_list, list):
            raise ValueError("scores_list must be a list")
        if not isinstance(time_of_delay_list, list):
            raise ValueError("time_of_delay_list must be a list")
        if not isinstance(cpu_time_list, list):
            raise ValueError("cpu_time_list must be a list")
        if not isinstance(labels_list, list):
            raise ValueError("labels_list must be a list")
        if not isinstance(benchmark_labels_list, list):
            raise ValueError("benchmark_labels_list must be a list")

    # overriding this to return tuples of (key,value)
    def __iter__(self):
        return iter([('name_algorithm', self.name_algorithm),
                     ('framerate', self.framerate),
                     ('total_time_of_acquisition', self.total_time_of_acquisition),
                     ('processor', self.processor),
                     ('processed_frames', self.processed_frames),
                     ('scores_list', self.scores_list),
                     ('time_of_delay_list', self.time_of_delay_list),
                     ('cpu_time_list', self.cpu_time_list),
                     ('labels_list', self.labels_list),
                     ('benchmark_labels_list', self.benchmark_labels_list)])

    def get_dict(self):
        return {'end2end': {self.name_algorithm: dict(self)}}

    def save(self, path):
        dict_object = dict(self)

        if os.path.isfile(path):
            warnings.warn('HDF5 file (' + path + ') already exists, it will be overwritten.')
        file_root = h5py.File(path, 'w')

        if not dict_object:
            raise TypeError('Object is empty!')

        for key, value in dict_object.items():
            if self._is_list_of_strings(value):
                file_root.create_dataset(key, data=np.array(value, dtype='S'))
            else:
                file_root.create_dataset(key, data=value)

        file_root.close()

    @staticmethod
    def _is_list_of_strings(lst):
        if not isinstance(lst, list):
            return False
        else:
            return bool(lst) and not isinstance(lst, basestring) and all(isinstance(elem, basestring) for elem in lst)
