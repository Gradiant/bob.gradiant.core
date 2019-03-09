#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.accesses.trimmer import Trimmer
from bob.gradiant.core.classes.accesses.framerate_modificator import FramerateModificator
from bob.gradiant.core.classes.accesses.timestamp_normalizer import TimestampNormalizer


class AccessModifier(object):

    def __init__(self, target_framerate=30, target_duration=-1, starting_time=-1, center_video_acquisition=False):
        """
        :param target_framerate: selected frame rate (default 30)
        :param target_duration: selected time to keep
        :param starting_time: selected point to start the video. Frames before this value will be discarded
        :param center_video_acquisition: Bool value. If True, it will ignore the starting_time value and crop the video
        from the central point.
        """
        self.target_framerate = target_framerate
        self.target_duration = target_duration
        self.starting_time = starting_time
        self.center_video_acquisition = center_video_acquisition

    def run(self, dict_images):
        dict_images = TimestampNormalizer.run(dict_images)
        dict_images = Trimmer.run(dict_images,
                                  target_duration=self.target_duration,
                                  starting_time=self.starting_time,
                                  center_video_acquisition=self.center_video_acquisition)
        dict_images = FramerateModificator.run(dict_images, target_framerate=self.target_framerate)
        return dict_images

    def __str__(self):
        message = 'AccessModifier [ '
        message += 'target_framerate = ' + str(self.target_framerate) + ' | '
        message += 'target_duration = ' + str(self.target_duration) + ' | '
        message += 'starting_time = ' + str(self.target_duration) + ' | '
        message += 'center_video_acquisition = ' + str(self.center_video_acquisition)
        message += ' ]'
        return message
