#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import time

from bob.gradiant.core import Colors, Informer


class UnitTestInformer(unittest.TestCase):

    def test_default_usage(self):
        title = 'access_name'
        informer = Informer(title)
        informer.message('message')
        informer.message('message_blue', color=Colors.FG.blue)

        total = 100
        for count in range(total + 1):
            informer.progress('loading', count, total, color=Colors.FG.green)
            time.sleep(0.01)








