#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain


class Trimmer(object):

    @staticmethod
    def assert_input(dict_images, target_duration):
        if not dict_images:
            raise ValueError("dict_images is empty")
        sorted_keys = sorted(dict_images.keys())
        if target_duration > sorted_keys[-1]:
            raise IndexError("target_duration must be lower than total duration")
        return sorted_keys

    @staticmethod
    def run(dict_images, target_duration=-1):
        sorted_keys = Trimmer.assert_input(dict_images, target_duration)
        trim_dict_images = {}
        if target_duration == -1:
            trim_dict_images = dict_images
        else:
            for key in sorted_keys:
                if key < target_duration:
                    trim_dict_images[key] = dict_images[key]
        return trim_dict_images