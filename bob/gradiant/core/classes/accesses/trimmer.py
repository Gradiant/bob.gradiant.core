#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.accesses.timestamp_normalizer import TimestampNormalizer
import numpy as np


def calculate_cropped_times(dict_images, target_duration):
    center_time = np.mean(list(dict_images))
    cropped_starting_time = center_time - float(target_duration/2)
    cropped_ending_time = center_time + float(target_duration/2)
    return cropped_starting_time, cropped_ending_time


class Trimmer(object):

    @staticmethod
    def assert_input(dict_images, target_duration, starting_time):
        if not dict_images:
            raise ValueError("dict_images is empty")
        sorted_keys = sorted(list(dict_images))
        if starting_time > sorted_keys[-1]:
            raise IndexError("starting_time ({}) must be lower than total duration ({})".format(starting_time,
                                                                                                sorted_keys[-1]))
        if target_duration > sorted_keys[-1]:
            raise IndexError("target_duration ({}) must be lower than total duration ({})".format(target_duration,
                                                                                                  sorted_keys[-1]))

    @staticmethod
    def run(dict_images, target_duration=-1, starting_time=-1, center_video_acquisition=False):
        """
        :param dict_images: images of the video sequence
        :param target_duration: selected time to keep
        :param starting_time: selected point to start the video. Frames before this value will be discarded
        :param center_video_acquisition: Bool value. If True, it will ignore the starting_time value and crop the video
        from the central point.
        :return: dict (key, image) with the filtered values
        """
        Trimmer.assert_input(dict_images, target_duration, starting_time)
        trimmed_dict_images = dict_images

        if center_video_acquisition:
            cropped_starting_time, cropped_ending_time = calculate_cropped_times(dict_images, target_duration)
            trim_dict_images = dict((key, value) for key, value in dict_images.items()
                                    if cropped_starting_time <= int(key) <= cropped_ending_time)
            trimmed_dict_images = TimestampNormalizer.run(trim_dict_images)
        else:
            if starting_time > 0:
                trim_dict_images = dict((key, value) for key, value in dict_images.items()
                                        if int(key) >= starting_time)
                trimmed_dict_images = TimestampNormalizer.run(trim_dict_images)

            if target_duration > 0:
                trimmed_dict_images = dict((key, value) for key, value in trimmed_dict_images.items()
                                           if int(key) <= target_duration)

        return trimmed_dict_images
