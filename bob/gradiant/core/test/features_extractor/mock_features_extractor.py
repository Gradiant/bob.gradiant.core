#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from bob.gradiant.core import FeaturesExtractor


class MockFeaturesExtractor(FeaturesExtractor):

    def __init__(self):
        super(MockFeaturesExtractor, self).__init__()

    def run(self, dict_images, annotations = None):
        pass
