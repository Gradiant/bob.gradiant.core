#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain


class FramerateModificator(object):

    @staticmethod
    def assert_inputs(dict_images, target_framerate):
        if not dict_images:
            raise ValueError("dict_images is empty")
        if target_framerate < 1:
            raise IndexError("target_framerate must be positive")

    @staticmethod
    def run(dict_images, target_framerate=30):
        FramerateModificator.assert_inputs(dict_images, target_framerate)

        dict_images_new_framerate = {}

        list_keys = sorted(dict_images.keys())

        temporal_gap = 1000/target_framerate
        target_range = range(list_keys[0],list_keys[-1]+temporal_gap,temporal_gap)

        for key in target_range:
            image = None
            if key in list_keys:
                last_it = list_keys.index(key)
                value = list_keys[last_it]
                image = dict_images[value]
            elif key > list_keys[-1]:
                break
            else:
                closest_number = min(list_keys, key=lambda x: abs(x - key))
                value = closest_number
                image = dict_images[value]
            if image is None:
                raise ValueError

            dict_images_new_framerate[value] = image

        return dict_images_new_framerate
