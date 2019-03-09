#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import h5py
import numpy as np
import os


class FeaturesSaver:
    base_path = None
    extension = '.h5'

    def __init__(self, base_path=None):
        if base_path is not None:
            self.set_base_path(base_path)

    def __str__(self):
        return '{} : {} , {}'.format(self.__class__.__name__, self.base_path.__str__(), self.extension.__str__())

    def save(self, basename_file, features_dict):
        if self.base_path is None:
            raise IOError('Base path is not set')

        if features_dict is None:
            raise TypeError('Error: entry dictionary is None!')

        self.assert_input(features_dict)

        filename = os.path.join(self.base_path, basename_file + self.extension)
        path, basename = os.path.split(filename)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != os.errno.EEXIST:
                    raise IOError(e.message)
        file_root = h5py.File(filename, 'w')
        sorted_keyframes = sorted(list(features_dict))

        features = []
        for keyframe in sorted_keyframes:
            value = features_dict[keyframe]
            if value is not None:
                value = np.ravel(value)
                value = np.expand_dims(value, axis=0)
                features.append(value)
        features = np.vstack(features)

        if features.size > 0:
            file_root.create_dataset('keyframe', data=np.array(sorted_keyframes, dtype='S'))
            features_dset = file_root.create_dataset('features', data=features)

            features_dset.attrs.create('single_feature_size', value.shape[0], dtype=int)

        file_root.close()

    @classmethod
    def assert_input(cls, features_dict):
        if features_dict is None:
            raise TypeError('features_dict dictionary is None!')
        if not features_dict:
            raise TypeError('features_dict dictionary is empty!')

    def file_exists(self, basename_file, ):
        filename = os.path.join(self.base_path, basename_file + self.extension)
        if os.path.isfile(filename):
            return True
        else:
            return False

    def set_base_path(self, base_path):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
