#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import numpy as np
from PIL import Image, ImageDraw


class TestUtils(object):
    resources_path = os.path.dirname(__file__)+'/../../../../resources'
    result_path = os.path.dirname(__file__)+'/../../../../result'

    @classmethod
    def get_resources_path(cls):
        return cls.resources_path

    @classmethod
    def get_result_path(cls):
        return cls.result_path

    @classmethod
    def get_image(cls, timestamp=None):
        image = Image.open(cls.resources_path + '/genuine/01.jpg')
        if timestamp:
            ImageDraw.Draw(
                image  # Image
            ).text(
                (0, 0),  # Coordinates
                'timestamp: {}'.format(timestamp),  # Text
                (0, 0, 0)  # Color
            )
        return image

    @classmethod
    def get_numpy_image(cls):
        return np.array(cls.get_image())

    @classmethod
    def get_synthetic_dict_image(cls, timestamp_reference=1500000000):
        dict_images = {}
        for timestamp in range(timestamp_reference, timestamp_reference+5000, 33):
            dict_images[timestamp] = cls.get_image(timestamp)
        return dict_images

    @classmethod
    def get_synthetic_dict_performance(cls):
        subset_list = ["dev"]
        n_samples = 10
        attack_list = ['print', 'all_attacks']
        metric_list = ['EER', 'HTER@EER', 'ACER@EER', 'APCER@EER', 'BPCER@EER']
        fps_list = np.array([10, 15, 30])
        tcapture_list = np.zeros([fps_list.size, n_samples])

        metric_value = np.zeros([len(attack_list), len(metric_list), fps_list.size, n_samples])

        metric_value[0, 0, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 0, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 0, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 0, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 0, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 0, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)

        metric_value[0, 1, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 1, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 1, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 1, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 1, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 1, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)

        tcapture_list[0, :] = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, -1]
        tcapture_list[1, :] = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, -1]
        tcapture_list[2, :] = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, -1]

        dict_performance = {}
        for i, subset in enumerate(subset_list):  # subset
            dict_performance[subset] = {}
            for j, attack in enumerate(attack_list):  # attacks
                dict_performance[subset][attack] = {}
                for k, metric in enumerate(metric_list):  # metric
                    dict_performance[subset][attack][metric] = {}
                    for l, fps in enumerate(fps_list):  # fps
                        dict_performance[subset][attack][metric][fps] = {}
                        for m in range(n_samples):
                            dict_performance[subset][attack][metric][fps][tcapture_list[l, m]] = {}
                            dict_performance[subset][attack][metric][fps][tcapture_list[l, m]]['value'] = metric_value[
                                j, k, l, m]
                            dict_performance[subset][attack][metric][fps][tcapture_list[l, m]]['threshold'] = 0.1
        return dict_performance

