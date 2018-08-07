#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import sys
from bob.gradiant.core.classes.informer.colors import Colors


class Informer(object):
    def __init__(self, title='informer', verbose=False, verbose_level=1):
        self.title = title
        self.verbose = verbose
        self.verbose_level = verbose_level

    def __str__(self):
        return '{} : title : {}, verbose : {}, verbose_level : {}'.format(self.__class__.__name__, self.title,
                                                                          self.verbose, self.verbose_level)

    def set_title(self, title):
        self.title = title

    def __reset(self):
        if self.verbose:
            sys.stdout.write('{}'.format(Colors.reset))

    def highlight_message(self, message, title=None, color=Colors.BG.cyan, prefix=Colors.bold, suffix='\n'):
        if self.verbose:
            if title:
                self.set_title(title)
            self.message(message,
                         color=color,
                         prefix=prefix,
                         suffix=suffix)

    def message(self, message, color=Colors.reset, prefix='', suffix=''):
        if self.verbose:
            self.__reset()
            sys.stdout.write('{}{}{} - {}{}{}'.format(prefix, color, self.title, message, Colors.reset, suffix))
            sys.stdout.flush()

    def progress(self, message, count, total, color=Colors.reset):
        if self.verbose:
            self.__reset()
            bar_len = 60
            filled_len = int(round(bar_len * count / float(total)))

            percents = round(100.0 * count / float(total), 1)
            bar = '=' * filled_len + '-' * (bar_len - filled_len)

            sys.stdout.write('{}{} - {} [{}]{}%\r'.format(color, self.title, message, bar, percents))

            if count >= total:
                sys.stdout.write('{}\n'.format(Colors.FG.black))
            sys.stdout.flush()

    def run(self, dict_images):
        raise NotImplementedError
