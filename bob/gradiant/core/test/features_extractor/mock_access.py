#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from bob.gradiant.core import Access


class MockAccess(Access):

    def __init__(self, path, name):
        super(MockAccess, self).__init__(path,name)

    def load(self):
        pass

    def load_annotations(self):
        pass
