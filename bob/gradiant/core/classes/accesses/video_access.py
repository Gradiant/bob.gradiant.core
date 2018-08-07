#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import numpy as np
import bob.io.video

from bob.gradiant.core.classes.accesses.access import Access
from bob.gradiant.core.classes.accesses.access_modificator import AccessModificator
from enum import Enum


class RotationRule(Enum):
    NO_ROTATION = 0
    ROTATION_90 = 1
    ROTATION_270 = 2


class VideoAccess(Access):

    def __init__(self, base_path, name, extension, access_modificator = AccessModificator(), rotation_rule = RotationRule.NO_ROTATION, annotation_base_path = None):
        if not os.path.isdir(base_path):
            raise IOError("Folder does not exist")
        if name is '':
            raise IOError("Name is empty")
        if not '.' in extension:
            raise IOError("extension is not valid. It must start with a point")
        self.extension = extension
        self.rotation_rule = rotation_rule
        self.selected_index = None
        super(VideoAccess,self).__init__(base_path,name, access_modificator, annotation_base_path = annotation_base_path)

    def __str__(self):
        return '{}/{}'.format(self.base_path,self.name)

    def set_access_modificator(self, access_modificator):
        if not isinstance(access_modificator, AccessModificator):
            raise TypeError("input must be a AccessModificator")
        self.access_modificator = access_modificator

    def load(self):
        dict_images = self.load_from_video()
        original_keys = dict_images.keys()
        dict_images = self.access_modificator.run(dict_images)
        if type(dict_images) is set:
            selected_keys = dict_images
        else:
            selected_keys = dict_images.keys()
        all_index = [int(val in selected_keys) for val in sorted(original_keys)]
        self.selected_index = [i for i, e in enumerate(all_index) if e != 0]
        return dict_images

    def load_annotations(self):
        annotations = None
        if self.annotation_base_path is None:
            filename_annotation = os.path.join(self.base_path, self.name + '.txt')
        else:
            filename_annotation = os.path.join(self.annotation_base_path, self.name + '.txt')
        if os.path.isfile(filename_annotation):
            eye_list = self.read_dlib_eyes_annotations(filename_annotation)
            if self.selected_index:
                eye_list = [eye_list[i] for i in self.selected_index]
            annotations = {'eyes_list': eye_list}
        return annotations

    def read_dlib_eyes_annotations(self, filename):
        with open(filename, 'r') as infile:
            data = infile.read()
            line_list = data.splitlines()

        eye_list = []
        for line in line_list:
            values_splitted = line.split(',')
            eye_left = (int(values_splitted[1]), int(values_splitted[2]))
            eye_right = (int(values_splitted[3]), int(values_splitted[4]))
            tuple_eyes = (eye_left, eye_right)
            eye_list.append(tuple_eyes)
        return eye_list

    def load_from_video(self):
        dict_images = {}
        filename_video = os.path.join(self.base_path, self.name + self.extension)

        if not os.path.isfile(filename_video):
            raise IOError("Impossible to load the video from this folder. It does not exist")
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
        gap = int(1000/fps)

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