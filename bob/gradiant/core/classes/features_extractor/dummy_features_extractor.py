#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from bob.gradiant.core.classes.features_extractor.features_extractor import FeaturesExtractor


class DummyFeaturesExtractor(FeaturesExtractor):

    def run(self, dict_images):
        dict_features = {}
        image = dict_images[list(dict_images)[0]]
        dict_features['feature'] = image[:10, 1, 1]
        return dict_features
