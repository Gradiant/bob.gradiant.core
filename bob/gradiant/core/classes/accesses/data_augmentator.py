#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import numpy as np
import copy


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


def flip_eyes_list(eyes_list):
    flipped_eyes_list = []
    for eye_tuple in eyes_list:
        flipped_eye_tuple = (eye_tuple[1], eye_tuple[0])
        flipped_eyes_list.append(flipped_eye_tuple)
    return flipped_eyes_list


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
        dict_augmented_data = {'original' : dict_images}
        if self.is_active:
            keys = dict_images.keys()
            values = dict_images.values()
            dict_augmented_data['reverse'] = dict(zip(keys, values[::-1]))
            dict_augmented_data['mirror'] = dict(zip(keys, [mirror(x) for x in values] ))
            dict_augmented_data['reverse-mirror'] = dict(zip(keys, [mirror(x) for x in values[::-1]]))

        return dict_augmented_data

    def augment_eyes_annotations(self, dict_annotations):
        dict_augmented_annotations = {'original': dict_annotations}
        if self.is_active:
            dict_augmented_annotations['reverse'] = dict_annotations
            dict_augmented_annotations['mirror'] = { 'eyes_list' : flip_eyes_list(dict_annotations['eyes_list'])}
            dict_augmented_annotations['reverse-mirror'] = { 'eyes_list' : flip_eyes_list(dict_annotations['eyes_list'])}

        return dict_augmented_annotations

    def get_all_suffixes(self):
        if self.is_active:
            return self.suffixes.values()
        else:
            return ['']

    def get_expanded_metadata(self, metadata):
        if self.is_active:
            expansion = {}
            for k, v in metadata.iteritems():
                expansion[k + '_r'] = v
                expansion[k + '_m'] = v
                expansion[k + '_rm'] = v

            metadata.update(expansion)
        return metadata

    def get_suffix(self, key):
        return self.suffixes[key]

    def __str__(self):
        message = 'AccessModificator [ '
        message += 'target_framerate = ' + str(self.target_framerate) + ' | '
        message += 'target_duration = ' + str(self.target_duration)
        message += ' ]'
        return message
