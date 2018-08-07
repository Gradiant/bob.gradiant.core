#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.accesses.framerate_modificator import FramerateModificator
from bob.gradiant.core.classes.accesses.trimmer import Trimmer
from bob.gradiant.core.classes.accesses.timestamp_normalizer import TimestampNormalizer


class AccessModificator(object):

    def __init__(self, target_framerate = 30, target_duration = -1):
        self.target_framerate = target_framerate
        self.target_duration = target_duration

    def run(self, dict_images):
        dict_images = TimestampNormalizer.run(dict_images)
        dict_images = Trimmer.run(dict_images, target_duration=self.target_duration)
        dict_images = FramerateModificator.run(dict_images, target_framerate=self.target_framerate)
        return dict_images

    def __str__(self):
        message = 'AccessModificator [ '
        message += 'target_framerate = ' + str(self.target_framerate) + ' | '
        message += 'target_duration = ' + str(self.target_duration)
        message += ' ]'
        return message

