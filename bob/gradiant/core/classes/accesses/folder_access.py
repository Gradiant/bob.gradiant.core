#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import h5py
import numpy as np

from PIL import Image

from bob.gradiant.core.classes.accesses.access import Access
from bob.gradiant.core.classes.accesses.access_modifier import AccessModifier


class FolderAccess(Access):
    def __init__(self,
                 base_path,
                 rgb_name,
                 extension='',
                 depth_name=None,
                 infrared_name=None,
                 access_modifier=AccessModifier(),
                 annotation_base_path=None,
                 database_name=None):

        self.folder_path = '/'.join([base_path, rgb_name])
        self._assert_input(self.folder_path, rgb_name, extension)
        self.extension = extension
        self.selected_index = None

        if depth_name is not None and infrared_name is not None:
            self.color_folder_path = self.folder_path
            self.depth_folder_path = '/'.join([base_path, depth_name])
            self.infrared_folder_path = '/'.join([base_path, infrared_name])

            self._assert_input(self.color_folder_path, rgb_name, extension)
            self._assert_input(self.depth_folder_path, depth_name, extension)
            self._assert_input(self.infrared_folder_path, infrared_name, extension)

        super(FolderAccess, self).__init__(base_path,
                                           rgb_name,
                                           access_modifier=access_modifier,
                                           annotation_base_path=annotation_base_path,
                                           database_name=database_name,
                                           )

    @staticmethod
    def _assert_input(folder_path, name, extension):
        if not os.path.isdir(folder_path) and not os.path.isfile(folder_path):
            raise IOError("Folder [] does not exist".format(folder_path))
        if name == '':
            raise IOError("Name is empty")
        if extension and '.' not in extension:
            raise IOError("extension [{}] is not valid. It must start with a point".format(extension))

    def set_access_modifier(self, access_modifier):
        if not isinstance(access_modifier, AccessModifier):
            raise TypeError("input must be a AccessModifier")
        self.access_modifier = access_modifier

    def load(self):
        try:
            dict_rgb_images = self.load_from_folder(self.color_folder_path)
            dict_depth_images = self.load_from_folder(self.depth_folder_path)
            dict_infrared_images = self.load_from_folder(self.infrared_folder_path)
            dict_images = {k: {'rgb': dict_rgb_images[k],
                               'depth': dict_depth_images[k],
                               'infrared': dict_infrared_images[k]}
                           for k in dict_rgb_images}

        except AttributeError:
            dict_images = self.load_from_folder(self.folder_path)
            original_keys = list(dict_images)
            dict_images = self.access_modifier.run(dict_images)
            if type(dict_images) is set:
                selected_keys = dict_images
            else:
                selected_keys = list(dict_images)
            all_index = [int(val in selected_keys) for val in sorted(original_keys)]
            self.selected_index = [i for i, e in enumerate(all_index) if e != 0]

        return dict_images

    def load_from_folder(self, folder_to_load):
        dict_images = {}
        if os.path.isdir(folder_to_load):
            list_files = os.listdir(folder_to_load)
            if len(list_files) == 0:
                raise IOError("Impossible to load any image from folder [{}]".format(folder_to_load))
            for file in list_files:
                if file.endswith(self.extension):
                    try:
                        key = self.get_key_from_file(file)
                        dict_images[key] = np.array(Image.open(os.path.join(folder_to_load, file)))
                    except:
                        continue
        else:
            dict_images[0] = np.array(Image.open(folder_to_load))

        if len(dict_images) == 0:
            raise IOError("Impossible to load any image from folder [{}]".format(folder_to_load))
        return dict_images

    def load_annotations(self):
        annotations = None
        annotations_path = os.path.join(self.base_path, self.name + '.h5')

        if os.path.isfile(annotations_path):
            annotations = self.read_mtcnn_annotations(annotations_path)
            for keyframe in annotations:
                annotations[keyframe] = {
                    'bbox': annotations[keyframe][0:4],
                    'landmarks': annotations[keyframe][4:-1],
                    'confidence': annotations[keyframe][14]
                }
        return annotations

    def read_mtcnn_annotations(self, filename):
        file_root = h5py.File(filename, 'r')
        mtcnn_results = np.asarray(file_root['features'])
        keyframes = np.asarray(file_root['keyframe']).tolist()

        dict_keyframes_annotations = {}
        for i, tstamp in enumerate(keyframes):
            dict_keyframes_annotations[tstamp] = mtcnn_results[i, :]

        return dict_keyframes_annotations

    def get_key_from_file(self, file):
        timestamp = file.split(".")[0]
        if timestamp is '':
            raise ValueError
        return int(timestamp)
