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
    def __assert_input(base_path, dict_ground_truth, dict_all_labels):
        if not os.path.isdir(base_path):
            raise IOError('base_path (' + base_path + ') does not exist')
        if not dict_ground_truth:
            raise ValueError('dict_ground_truth is empty')
        if not dict_all_labels:
            raise ValueError('dict_all_labels is empty')

    @staticmethod
    def run(base_path, dict_ground_truth, dict_all_labels, database_name_list=['']):
        """
            base_path: path where features are stored
            dict_ground_truth: ground truth given by the protocol
            dict_all_labels:
               e.g        {'Train': {'grad_001_real_00_00': {'user': 1,
                                                            'pai': 0,
                                                            'common_pai': 0,
                                                            'capture_device': 3,
                                                            'common_capture_device': 0,
                                                            'scenario': 3,
                                                            'light': 1},

                                    'grad_002_attack_02_00': {'user': 2,
                                                              'pai': 0,
                                                              'common_pai': 1,
                                                              'capture_device': 3,
                                                              'common_capture_device': 0,
                                                              'scenario': 3,
                                                              'light': 1},

                                    'grad_003_real_00_00': {'user': 3,
                                                            'pai': 0,
                                                            'common_pai': 0,
                                                            'capture_device': 3,
                                                            'common_capture_device': 0,
                                                            'scenario': 3,
                                                            'light': 1}
                                    }
                          }
            database_name_list: specific database folder. e.g ['replay-mobile', 'replay-attack', ...]
                                by default is [''], it means that is that features are already in the base path
        """
        PipelineFeaturesFormatLoader.__assert_input(base_path, dict_ground_truth, dict_all_labels)

        pipeline_dict = {}
        access_id = 0

        for subset, dict_labeled_basenames in dict_ground_truth.items():
            common_pai = np.array([])
            common_capture_device = np.array([])
            db_labels = np.array([])
            all_features = np.array([])
            all_keyframes = np.array([])
            all_access_ids = np.array([])
            all_access_names = np.array([])

            list_retrieved_features = []
            list_retrieved_keyframe = []

            max_columns_accesses = PipelineFeaturesFormatLoader.get_max_columns_accesses(dict_all_labels)

            for basename, label in dict_labeled_basenames.items():
                for folder_database in database_name_list:
                    full_path = os.path.join(base_path, folder_database)
                    filename = os.path.join(full_path, basename + '.h5')
                    try:
                        file_root = h5py.File(filename, 'r')
                        features_added = False
                        if 'features' in file_root.keys():
                            retrieved_features = file_root['features']
                            list_retrieved_features.append(retrieved_features[...])
                            features_added = True

                        if 'keyframe' in file_root.keys():
                            retrieved_keyframe = file_root['keyframe'][...]
                            if PipelineFeaturesFormatLoader._is_numpy_array_of_bytestrings(retrieved_keyframe):
                                retrieved_keyframe = [x.decode('utf-8') for x in retrieved_keyframe]
                            list_retrieved_keyframe.append(retrieved_keyframe)
                    except (IOError, OSError):
                        continue

                    if features_added:
                        len_features = retrieved_features.shape[0]

                        common_pai = PipelineFeaturesFormatLoader.repeat_and_concatenate_labels(len_features,
                                                                                                dict_all_labels[subset][basename]['common_pai'],
                                                                                                common_pai)
                        common_capture_device = \
                            PipelineFeaturesFormatLoader.repeat_and_concatenate_labels(len_features,
                                                                                       dict_all_labels[subset][basename]['common_capture_device'],
                                                                                       common_capture_device)

                        labels_row = PipelineFeaturesFormatLoader.get_concatenated_db_labels_from_dict(
                            dict_all_labels[subset][basename])
                        current_columns = labels_row.shape[0]
                        if current_columns < max_columns_accesses:
                            difference_to_fill = max_columns_accesses - current_columns
                            filler_values = difference_to_fill * [np.nan]
                            labels_row = np.append(labels_row, filler_values)

                        db_labels = PipelineFeaturesFormatLoader.repeat_and_concatenate_labels(len_features, labels_row,
                                                                                               db_labels,
                                                                                               label_is_row=True)

                        all_access_ids = PipelineFeaturesFormatLoader.repeat_and_concatenate_labels(len_features,
                                                                                                    access_id,
                                                                                                    all_access_ids)

                        access_names = np.repeat(basename, len_features, axis=0)
                        all_access_names = np.append(all_access_names,
                                                     access_names) if all_access_names.size else access_names

                    access_id += 1
                    file_root.close()

            if len(list_retrieved_features) > 0:
                all_features = np.vstack(list_retrieved_features)
            if len(list_retrieved_keyframe) > 0:
                all_keyframes = np.concatenate(list_retrieved_keyframe)

            pipeline_dict[subset] = {'features': all_features,
                                     'keyframes': all_keyframes,
                                     'db_labels': db_labels,
                                     'common_pai': common_pai,
                                     'common_capture_device': common_capture_device,
                                     'access_ids': all_access_ids,
                                     'access_names': all_access_names}
        return pipeline_dict

    @staticmethod
    def assert_pipeline_dict(pipeline_dict):
        for subset, dict_features in pipeline_dict.items():
            for key, value in dict_features.items():
                if value.size == 0:
                    raise ValueError('PipelineFeaturesFormatLoader: It was not able to load any feature. {} value '
                                     'cannot be empty ({} subset)'.format(key, subset))

    @staticmethod
    def get_max_columns_accesses(dict_all_labels):
        max_columns = 0
        for subset, dict_basenames in dict_all_labels.items():
            for key, row_labels in dict_basenames.items():
                labels_row = PipelineFeaturesFormatLoader.get_concatenated_db_labels_from_dict(row_labels)
                max_columns_tmp = labels_row.shape[0]
                if max_columns_tmp > max_columns:
                    max_columns = max_columns_tmp
        return max_columns

    @staticmethod
    def repeat_and_concatenate_labels(len_features, label, all, label_is_row=False):
        if label_is_row:
            access = np.tile(label, (len_features, 1))
            all = np.vstack((all, access)) if all.size else access
        else:
            access = np.ones(len_features, np.int) * label
            all = np.append(all, access) if all.size else access
        return all

    @staticmethod
    def get_concatenated_db_labels_from_dict(dict_labels_subset_basename):
        __KEYS_TO_IGNORE = ['pai', 'scenario', 'user', 'capture_device', 'common_pai', 'common_capture_device']
        labels_row = [dict_labels_subset_basename['pai'], dict_labels_subset_basename['scenario'],
                      dict_labels_subset_basename['user'], dict_labels_subset_basename['capture_device']]

        # alphabetically ordering of the rest of labels
        for key in sorted(dict_labels_subset_basename.keys()):
            if key in __KEYS_TO_IGNORE:
                continue
            else:
                labels_row.append(dict_labels_subset_basename[key])

        return np.asarray(labels_row)

    @staticmethod
    def _is_numpy_array_of_bytestrings(arr):
        if not isinstance(arr, np.ndarray):
            return False
        elif np.issubdtype(arr.dtype, np.str_):
            return True
        else:
            return False
