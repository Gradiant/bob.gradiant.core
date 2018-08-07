#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
from bob.gradiant.core.classes.evaluation.data.pad.experiment_result import ExperimentResult

class ExperimentResultLoader(object):

    @staticmethod
    def load_from_folder(base_path):
        if not os.path.isdir(base_path):
            raise IOError('base_path is not a dir')
        included_extensions = ['h5']
        list_filenames = [fn for fn in os.listdir(base_path)
                          if any(fn.endswith(ext) for ext in included_extensions)]

        list_experiment_result = []
        for filename in list_filenames:
            path_filename = os.path.join(base_path, filename)
            list_experiment_result.append(ExperimentResult.load(path_filename))

        return list_experiment_result