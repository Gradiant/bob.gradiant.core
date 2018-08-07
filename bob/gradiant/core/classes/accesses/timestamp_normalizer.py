#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain


class TimestampNormalizer(object):

    @staticmethod
    def assert_inputs(dict_images):
        if not dict_images:
            raise ValueError("dict_images is empty")

    @staticmethod
    def run(dict_images):
        TimestampNormalizer.assert_inputs(dict_images)

        sorted_list_keys = sorted(dict_images.keys())
        bias = sorted_list_keys[0]
        normalized_dict_images = {}
        for key, value in dict_images.iteritems():
            normalized_dict_images[key-bias] = dict_images[key]
        return normalized_dict_images
