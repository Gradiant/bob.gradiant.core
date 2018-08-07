#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from bob.gradiant.core.classes.accesses.access import Access
from bob.gradiant.core.classes.accesses.data_augmentator import DataAugmentator
from bob.gradiant.core.classes.features_extractor.features_extractor import FeaturesExtractor
from bob.gradiant.core.classes.informer.colors import Colors
from bob.gradiant.core.classes.informer.informer import Informer
from bob.gradiant.core.classes.storage.features_saver import FeaturesSaver

DOTS = '.' * 20
SPACES = ' '*20

class FeaturesExtractorManager:
    base_path = None

    def __init__(self, features_extractor, features_saver):
        self.assert_input(features_extractor, features_saver)
        self.features_extractor = features_extractor
        self.features_saver = features_saver

    def __str__(self):
        return '{} : {} , {}'.format(self.__class__.__name__, self.features_extractor.__str__(),
                                     self.features_saver.__str__())

    @classmethod
    def assert_input(cls, features_extractor, features_saver):
        if not isinstance(features_extractor, FeaturesExtractor):
            raise TypeError("input must be a FeaturesExtractor")
        if not isinstance(features_saver, FeaturesSaver):
            raise TypeError("input must be a FeaturesSaver")

    def run(self, access, informer=Informer(), recreate=False, data_augmentator=DataAugmentator()):
        if not isinstance(access, Access):
            raise TypeError("input must be a Access")

        if self.is_already_extracted(access, recreate, data_augmentator):
            informer.message('already extracted' + SPACES, color=Colors.FG.lightgrey, suffix='\r')
        else:
            dict_images_original = access.load()
            dict_annotations = access.load_annotations()
            dict_augmented_data = data_augmentator.augment_sequences(dict_images_original)
            dict_augmented_annotations = data_augmentator.augment_eyes_annotations(dict_annotations)
            for key, dict_images in dict_augmented_data.iteritems():
                informer.message('processing [' + str(len(dict_images.keys()))+ ' images]' + DOTS, color=Colors.bold, suffix='\r')

                dict_features = self.features_extractor.run(dict_images, annotations = dict_augmented_annotations[key])

                if len(dict_features)>0:
                    name = access.name + data_augmentator.get_suffix(key)
                    self.features_saver.save(name, dict_features)

    def is_already_extracted(self,access, recreate, data_augmentator):
        if recreate:
            return False
        for suffix in data_augmentator.get_all_suffixes():
            if not self.features_saver.file_exists(access.name+suffix):
                return False
        return True

    def set_base_path(self, base_path):
        self.base_path = base_path
        self.features_saver.set_base_path(base_path)

    def get_feature_extractor_name(self):
        return self.features_extractor.name
