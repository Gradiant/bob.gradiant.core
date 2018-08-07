#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import h5py
import os
import numpy as np


class PipelineFeaturesFormatLoader:

    def __init__(self):
        pass

    @staticmethod
    def __assert_input(base_path, dict_labeled_basenames):
        if not os.path.isdir(base_path):
            raise IOError('base_path (' + base_path + ') does not exist')
        if not dict_labeled_basenames:
            raise ValueError('dict_labeled_basenames is empty')

    @staticmethod
    def run(base_path, dict_subset_labeled_basenames):
        PipelineFeaturesFormatLoader.__assert_input(base_path, dict_subset_labeled_basenames)

        pipeline_dict = {}
        access_id = 0
        for subset, dict_labeled_basenames in dict_subset_labeled_basenames.iteritems():
            all_features = np.array([])
            all_labels = np.array([])
            all_keyframes = np.array([])
            all_access_ids = np.array([])

            list_retrieved_features = []
            list_retrieved_keyframe = []
            for basename, label in dict_labeled_basenames.iteritems():
                filename = os.path.join(base_path,basename + '.h5')
                try:
                    file_root = h5py.File(filename, 'r')
                    features_added = False

                    if 'features' in file_root.keys():
                        retrieved_features = file_root['features']
                        list_retrieved_features.append(retrieved_features[...])
                        features_added = True

                    if 'keyframe' in file_root.keys():
                        retrieved_keyframe = file_root['keyframe']
                        list_retrieved_keyframe.append(retrieved_keyframe[...])
                except:
                    continue

                if (features_added):
                    len_features = retrieved_features.shape[0]
                    access_labels = np.ones(len_features,np.int)*label
                    all_labels = np.append(all_labels, access_labels) if all_labels.size else access_labels
                    access_ids = np.ones(len_features,np.int)*access_id
                    all_access_ids = np.append(all_access_ids, access_ids) if all_access_ids.size else access_ids

                access_id += 1

            if len(list_retrieved_features) > 0:
                all_features = np.vstack(list_retrieved_features)
            if len(list_retrieved_keyframe)>0:
                all_keyframes = np.concatenate(list_retrieved_keyframe)

            pipeline_dict[subset] = {'features': all_features, 'labels': all_labels, 'keyframes': all_keyframes, 'access_ids' : all_access_ids}

        return pipeline_dict


