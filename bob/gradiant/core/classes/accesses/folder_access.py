#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import numpy as np

from PIL import Image

from bob.gradiant.core.classes.accesses.access import Access
from bob.gradiant.core.classes.accesses.access_modificator import AccessModificator


class FolderAccess(Access):
    def __init__(self, base_path, name, extension = '', access_modificator = AccessModificator(), annotation_base_path = None):
        self.folder_path = '/'.join([base_path, name])
        if not os.path.isdir(self.folder_path):
            raise IOError("Folder does not exist")
        if name == '':
            raise IOError("Name is empty")
        if extension and not '.' in extension:
            raise IOError("extension is not valid. It must start with a point")
        self.extension = extension
        self.selected_index = None
        super(FolderAccess,self).__init__(base_path,name, access_modificator=access_modificator, annotation_base_path=annotation_base_path)

    def set_access_modificator(self, access_modificator):
        if not isinstance(access_modificator, AccessModificator):
            raise TypeError("input must be a AccessModificator")
        self.access_modificator = access_modificator

    def load(self):
        dict_images = self.load_from_folder()
        original_keys = dict_images.keys()
        dict_images = self.access_modificator.run(dict_images)
        if type(dict_images) is set:
            selected_keys = dict_images
        else:
            selected_keys = dict_images.keys()
        all_index = [int(val in selected_keys) for val in sorted(original_keys)]
        self.selected_index = [i for i, e in enumerate(all_index) if e != 0]
        return dict_images

    def load_from_folder(self):
        dict_images = {}
        list_files = os.listdir(self.folder_path)
        if len(list_files) == 0:
            raise IOError("Impossible to load any image from this folder")
        for file in list_files:
            if file.endswith(self.extension):
                try:
                    key = self.get_key_from_file(file)
                    dict_images[key] = np.array(Image.open(os.path.join(self.folder_path, file)))
                except:
                    continue
        if len(dict_images) == 0:
            raise IOError("Impossible to load any image from this folder")
        return dict_images

    def load_annotations(self):
        annotations = None
        if self.annotation_base_path is None:
          filename_annotation = os.path.join(self.base_path, self.name + '.txt')
        else:
          filename_annotation = os.path.join(self.annotation_base_path, self.name + '.txt')

        if os.path.isfile(filename_annotation):
            eye_list = self.read_dlib_eyes_annotations(filename_annotation)
            if self.selected_index:
                eye_list = [eye_list[i] for i in self.selected_index]
            annotations = {'eyes_list': eye_list}
        return annotations

    def get_key_from_file(self, file):
        timestamp =file.split(".")[0]
        if timestamp is '':
            raise ValueError
        return int(timestamp)
