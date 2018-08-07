#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

class PadInfo(object):
    def __init__(self, type_attacks, framerate, time_capture):
        self.assert_input(type_attacks, framerate, time_capture)
        self.type_attacks = type_attacks
        self.framerate = framerate
        self.time_capture = time_capture

    @classmethod
    def assert_input(cls, type_attacks, framerate, time_capture):
        if not type_attacks:
            raise TypeError('list_attacks is empty')
        if framerate < 0:
            raise TypeError('framerate must be positive')
        if time_capture < -1:
            raise TypeError('time_capture must be always positive (unless -1, which represents standard evaluation with whole video)')

    def __str__(self):
        return '{} : type_attacks : {}, framerate : {}, time_capture : {}'.format(self.__class__.__name__,self.type_attacks, self.framerate,self.time_capture)