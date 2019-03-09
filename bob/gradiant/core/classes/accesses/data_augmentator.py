#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import copy
import numpy as np


def mirror(image_original):
    image = copy.deepcopy(image_original)
    frame_mirror = image
    if image.ndim == 1:
        frame_mirror = np.fliplr(image)
    else:
        frame_mirror[0] = np.fliplr(image[0])
        frame_mirror[1] = np.fliplr(image[1])
        frame_mirror[2] = np.fliplr(image[2])
    return frame_mirror


def flip_mtcnn_annotations(dict_annotations, dict_images):
    dict_augmented_annotations = copy.deepcopy(dict_annotations)

    for keyframe in dict_annotations:
        if dict_augmented_annotations['confidence'] != 0.0:
            width = dict_images[keyframe].shape[1]

            dict_augmented_annotations['bbox'][0] = width - dict_augmented_annotations['bbox'][0]
            dict_augmented_annotations['bbox'][2] = width - dict_augmented_annotations['bbox'][2]

            dict_augmented_annotations['landmarks'][0] = width - dict_augmented_annotations['landmarks'][0]
            dict_augmented_annotations['landmarks'][2] = width - dict_augmented_annotations['landmarks'][2]
            dict_augmented_annotations['landmarks'][4] = width - dict_augmented_annotations['landmarks'][4]
            dict_augmented_annotations['landmarks'][6] = width - dict_augmented_annotations['landmarks'][6]
            dict_augmented_annotations['landmarks'][8] = width - dict_augmented_annotations['landmarks'][8]

    return dict_augmented_annotations


class DataAugmentator(object):
    suffixes = {
        'original': '',
        'reverse': '_r',
        'mirror': '_m',
        'reverse-mirror': '_rm'
    }

    def __init__(self, is_active=False):
        self.is_active = is_active

    def augment_sequences(self, dict_images):
        dict_augmented_data = {'original': dict_images}
        if self.is_active:
            keys = list(dict_images)
            values = list(dict_images.values())
            dict_augmented_data['reverse'] = dict(zip(keys, values[::-1]))
            dict_augmented_data['mirror'] = dict(zip(keys, [mirror(x) for x in values]))
            dict_augmented_data['reverse-mirror'] = dict(zip(keys, [mirror(x) for x in values[::-1]]))

        return dict_augmented_data

    def augment_annotations(self, dict_annotations, dict_images):
        dict_augmented_annotations = {'original': dict_annotations}
        if self.is_active:
            dict_augmented_annotations['reverse'] = dict_annotations
            dict_augmented_annotations['mirror'] = flip_mtcnn_annotations(dict_annotations, dict_images)
            dict_augmented_annotations['reverse-mirror'] = flip_mtcnn_annotations(dict_annotations, dict_images)

        return dict_augmented_annotations

    def get_all_suffixes(self):
        if self.is_active:
            return self.suffixes.values()
        else:
            return ['']

    def get_expanded_metadata(self, metadata):
        if self.is_active:
            expansion = {}
            for k, v in metadata.items():
                expansion[k + '_r'] = v
                expansion[k + '_m'] = v
                expansion[k + '_rm'] = v

            metadata.update(expansion)
        return metadata

    def get_suffix(self, key):
        return self.suffixes[key]

    def __str__(self):
        message = 'AccessModifier [ '
        message += 'target_framerate = ' + str(self.target_framerate) + ' | '
        message += 'target_duration = ' + str(self.target_duration)
        message += ' ]'
        return message
