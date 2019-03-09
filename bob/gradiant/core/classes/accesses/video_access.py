#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import h5py
import numpy as np
import bob.io.video

from bob.gradiant.core.classes.accesses.access import Access
from bob.gradiant.core.classes.accesses.access_modifier import AccessModifier
from enum import Enum


class RotationRule(Enum):
    NO_ROTATION = 0
    ROTATION_90 = 1
    ROTATION_270 = 2


class VideoAccess(Access):

    def __init__(self,
                 base_path,
                 name,
                 extension,
                 access_modifier=AccessModifier(),
                 rotation_rule=RotationRule.NO_ROTATION,
                 annotation_base_path=None,
                 database_name=None):
        if not os.path.isdir(base_path):
            raise IOError("Folder [] does not exist".format(base_path))
        if name is '':
            raise IOError("Name is empty")
        if extension and '.' not in extension:
            raise IOError("extension [{}] is not valid. It must start with a point".format(extension))
        self.extension = extension
        self.rotation_rule = rotation_rule
        self.selected_index = None
        super(VideoAccess, self).__init__(base_path,
                                          name,
                                          access_modifier,
                                          annotation_base_path=annotation_base_path,
                                          database_name=database_name)

    def __str__(self):
        return '{}/{}'.format(self.base_path, self.name)

    def set_access_modifier(self, access_modifier):
        if not isinstance(access_modifier, AccessModifier):
            raise TypeError("input must be a AccessModifier")
        self.access_modifier = access_modifier

    def load(self):
        dict_images = self.load_from_video()
        original_keys = list(dict_images)
        dict_images = self.access_modifier.run(dict_images)
        if type(dict_images) is set:
            selected_keys = dict_images
        else:
            selected_keys = list(dict_images)
        all_index = [int(val in selected_keys) for val in sorted(original_keys)]
        self.selected_index = [i for i, e in enumerate(all_index) if e != 0]
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

    @staticmethod
    def read_mtcnn_annotations(filename):
        file_root = h5py.File(filename, 'r')
        mtcnn_results = np.asarray(file_root['features'])
        keyframes = np.asarray(file_root['keyframe']).tolist()

        dict_keyframes_annotations = {}
        for i, tstamp in enumerate(keyframes):
            dict_keyframes_annotations[tstamp] = mtcnn_results[i, :]

        return dict_keyframes_annotations

    def load_from_video(self):
        dict_images = {}
        filename_video = os.path.join(self.base_path, self.name + self.extension)

        if not os.path.isfile(filename_video):
            raise IOError("Impossible to load the video from folder []. It does not exist"
                          .format(filename_video))
        counter = 0

        reader = bob.io.video.reader(filename_video)
        fps = reader.frame_rate
        vin = reader.load()

        if self.rotation_rule is RotationRule.ROTATION_270:
            vin = np.rollaxis(vin, 3, 2)

        if self.rotation_rule is RotationRule.ROTATION_90:
            vin = np.rollaxis(vin, 3, 2)
            vin = vin[:, :, ::-1, :]

        vin = np.swapaxes(np.swapaxes(vin, 1, 2), 2, 3)
        gap = int(1000 / fps)

        try:
            for k in range(vin.shape[0]):
                frame = vin[k, :, :, :]
                dict_images[counter] = frame
                counter += gap
        except RuntimeError:
            pass

        if len(dict_images) == 0:
            raise IOError("Impossible to load the video file")
        return dict_images
