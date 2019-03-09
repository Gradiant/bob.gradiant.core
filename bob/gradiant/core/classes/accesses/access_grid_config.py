# coding=utf-8
from sklearn.model_selection import ParameterGrid


class AccessGridConfig:

    def __init__(self,
                 framerate_list=[15],
                 total_time_acquisition_list=[2000],
                 starting_time_acquisition_list=[-1],
                 center_video_acquisition_list=[True]):
        """
        This class contains the configuration in order to setup our experiments.
        This class will combine the options (params) to modify the accesses (video)
        consistently with the params.

        Default parameters will filter the video from the center, using 2000 ms and 15 frames per second.


        :param framerate_list: a list with a selected frame rates (default [15])
        :param total_time_acquisition_list: a list with selected times to keep (default [2000] <- 2s)
        :param starting_time_acquisition_list: a list with selected points to start the video.
        Frames before this value will be discarded. (default [-1] <- ignore this parameter)
        :param center_video_acquisition_list: Bool value. If True, it will ignore the starting_time value and crop the video
        from the central point. (default [True])
        """
        self.__assert_inputs(framerate_list,
                             total_time_acquisition_list,
                             starting_time_acquisition_list,
                             center_video_acquisition_list)
        self.framerate_list = framerate_list
        self.total_time_acquisition_list = total_time_acquisition_list
        self.starting_time_acquisition_list = starting_time_acquisition_list
        self.center_video_acquisition_list = center_video_acquisition_list
        self.parameter_grid = list(ParameterGrid({'framerate': self.framerate_list,
                                                  'total_time_acquisition': self.total_time_acquisition_list,
                                                  'starting_time_acquisition': self.starting_time_acquisition_list,
                                                  'center_video_acquisition': self.center_video_acquisition_list}))

    def __assert_inputs(self,
                        framerate_list,
                        total_time_acquisition_list,
                        starting_time_acquisition_list,
                        center_video_acquisition_list):
        if framerate_list is None:
            raise TypeError('framerate_list is not defined (None Value).')
        else:
            if type(framerate_list) is not list:
                raise TypeError('framerate_list must be defined as a list')

        if total_time_acquisition_list is None:
            raise TypeError('total_time_acquisition_list is not defined (None Value).')
        else:
            if type(total_time_acquisition_list) is not list:
                raise TypeError('total_time_acquisition_list must be defined as a list.')

        if starting_time_acquisition_list is None:
            raise TypeError('starting_time_acquisition_list is not defined (None Value).')
        else:
            if type(starting_time_acquisition_list) is not list:
                raise TypeError('starting_time_acquisition_list must be defined as a list.')

        if center_video_acquisition_list is None:
            raise TypeError('center_video_acquisition_list is not defined (None Value).')
        else:
            if type(starting_time_acquisition_list) is not list:
                raise TypeError('center_video_acquisition_list must be defined as a list.')

    @staticmethod
    def get_config_summary_from_parameters_entry(parameters):
        last_param = ""
        if parameters["center_video_acquisition"]:
            last_param = "_centered"
        else:
            if parameters["starting_time_acquisition"] > 0:
                last_param = "_startingtime{}".format(parameters["starting_time_acquisition"])

        summary = "framerate{}_duration{}{}".format(parameters["framerate"],
                                                    parameters["total_time_acquisition"],
                                                    last_param)
        return summary

    def get_message_summary_parameter_grid(self):
        return '{} configurations from {} , {},  {} and {}'.format(len(self.parameter_grid),
                                                                   self.framerate_list,
                                                                   self.starting_time_acquisition_list,
                                                                   self.total_time_acquisition_list,
                                                                   self.center_video_acquisition_list)

    def get_format_message_from_parameters(self, parameters):
        return 'framerate : {} | ' \
               'starting_time_acquisition: {} | ' \
               'total_time_acquisition: {} | ' \
               'center_video_acquisition_list: {}'.format(parameters['framerate'],
                                                          parameters['starting_time_acquisition'],
                                                          parameters['total_time_acquisition'],
                                                          parameters['center_video_acquisition'])

    def get_parameter_grid(self):
        return self.parameter_grid
