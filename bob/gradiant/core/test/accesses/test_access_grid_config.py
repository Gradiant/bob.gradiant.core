#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest

from bob.gradiant.core import AccessGridConfig
from sklearn.model_selection import ParameterGrid


class UnitTestAccessGridConfig(unittest.TestCase):

    def test_should_throw_an_exception_if_parameters_are_none_or_not_a_list(self):
        parameters_grid = list(ParameterGrid({'framerate_list': [None, "wrong"],
                                              'total_time_acquisition': [None, "wrong"],
                                              'starting_time_acquisition': [None, "wrong"],
                                              'center_video_acquisition': [None, "wrong"]}))
        for parameters in parameters_grid:
            self.assertRaises(TypeError,
                              lambda: AccessGridConfig(parameters["framerate_list"],
                                                       parameters["total_time_acquisition"],
                                                       parameters["starting_time_acquisition"],
                                                       parameters["center_video_acquisition"]
                                                       )
                              )

    def test_should_return_a_valid_parameter_grid_with_default_constructor(self):
        access_grid_config = AccessGridConfig()

        parameter_grid = access_grid_config.get_parameter_grid()

        self.assertEqual(len(parameter_grid), 1)
        parameter = parameter_grid[0]
        self.assertEqual(parameter["framerate"], 15)
        self.assertEqual(parameter["total_time_acquisition"], 2000)
        self.assertEqual(parameter["starting_time_acquisition"], -1)
        self.assertEqual(parameter["center_video_acquisition"], True)

    def test_should_return_a_valid_parameter_grid_with_parametrized_constructor(self):
        access_grid_config = AccessGridConfig(framerate_list=[30, 15],
                                              total_time_acquisition_list=[500, 1000],
                                              starting_time_acquisition_list=[100, 200],
                                              center_video_acquisition_list=[False])

        parameter_grid = access_grid_config.get_parameter_grid()

        self.assertEqual(len(parameter_grid), 8)

    def test_should_return_a_valid_summary_with_default_constructor(self):
        access_grid_config = AccessGridConfig()
        parameter_grid = access_grid_config.get_parameter_grid()
        parameter = parameter_grid[0]

        summary = access_grid_config.get_config_summary_from_parameters_entry(parameter)

        self.assertEqual(summary, "framerate15_duration2000_centered")

    def test_should_return_a_valid_summary_with_starting_time_acquisition_list_1000_and_center_video_acquisition_list_false(self):
        access_grid_config = AccessGridConfig(starting_time_acquisition_list=[1000],
                                              center_video_acquisition_list=[False])
        parameter_grid = access_grid_config.get_parameter_grid()
        parameter = parameter_grid[0]

        summary = access_grid_config.get_config_summary_from_parameters_entry(parameter)

        self.assertEqual(summary, "framerate15_duration2000_startingtime1000")


