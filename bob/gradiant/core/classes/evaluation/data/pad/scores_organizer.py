#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import numpy as np
import copy
from sklearn.model_selection import ParameterGrid

from bob.gradiant.core.classes.evaluation.data.pad.pad_data import PadData
from bob.gradiant.core.classes.evaluation.data.pad.pad_info import PadInfo
from bob.gradiant.core.classes.evaluation.data.pad.scores_container import ScoresContainer
from bob.gradiant.core.classes.evaluation.data.pad.subset_data import SubsetData

ALL_ATTACKS_NAME = 'all_attacks'


def get_combinations(list_experiment_result):
    list_framerate = [experiment_result.framerate for experiment_result in list_experiment_result]
    list_time_capture = [experiment_result.time_capture for experiment_result in list_experiment_result]

    attacks_correspondences = list_experiment_result[0].attacks_correspondences

    return np.unique(list_framerate), np.unique(list_time_capture), attacks_correspondences


def filter_by_framerate_and_time_capture(list_experiment_result, framerate, time_capture):
    filtered_list_experiment_result = copy.deepcopy(list_experiment_result)
    filtered_list_experiment_result = [experiment_result for experiment_result in filtered_list_experiment_result if
                                       experiment_result.framerate == framerate and experiment_result.time_capture == time_capture]
    return filtered_list_experiment_result


def get_score_container_filtered_by_type_attack(list_experiment_result, type_attack, attacks_correspondences):
    scores = np.array([])
    labels = np.array([])

    for experiment_result in list_experiment_result:
        scores_genuine = experiment_result.scores[experiment_result.common_pai == 0]
        scores = np.append(scores, scores_genuine)
        labels = np.append(labels, np.zeros(len(scores_genuine), dtype=int))

        if type_attack == ALL_ATTACKS_NAME:
            reference_labels = np.unique(experiment_result.common_pai)
            for label in reference_labels.tolist():
                if label != 0:
                    scores_attack = experiment_result.scores[experiment_result.common_pai == label]
                    scores = np.append(scores, scores_attack)
                    labels = np.append(labels, label * np.ones(len(scores_attack), dtype=int))
        else:
            index_label = attacks_correspondences[type_attack]
            scores_attack = experiment_result.scores[experiment_result.common_pai == index_label]
            scores = np.append(scores, scores_attack)
            labels = np.append(labels, index_label * np.ones(len(scores_attack), dtype=int))

        if experiment_result.is_distance:
            scores = -scores

    return ScoresContainer(scores, labels)


class ScoresOrganizer(object):

    @staticmethod
    def run(list_experiment_result):
        if not list_experiment_result:
            raise TypeError('list_experiment_result is empty')
        list_pad_data = []

        list_framerate, list_time_capture, attacks_correspondences = get_combinations(list_experiment_result)
        list_attacks = [ALL_ATTACKS_NAME] + list(attacks_correspondences)

        parameters_grid = list(ParameterGrid(
            {'type_attack': list_attacks, 'framerate': list_framerate, 'time_capture': list_time_capture}))
        for parameters in parameters_grid:
            pad_info = PadInfo(parameters['type_attack'], parameters['framerate'], parameters['time_capture'])

            filtered_list_experiment_result = filter_by_framerate_and_time_capture(list_experiment_result,
                                                                                   parameters['framerate'],
                                                                                   parameters['time_capture'])
            scores_container = get_score_container_filtered_by_type_attack(filtered_list_experiment_result,
                                                                           parameters['type_attack'],
                                                                           attacks_correspondences)

            pad_data = PadData(pad_info, scores_container)
            list_pad_data.append(pad_data)

        subset_data = SubsetData(parameters_grid, list_pad_data)
        return subset_data
