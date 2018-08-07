#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

import collections

from bob.gradiant.core.classes.evaluation.data.pad.experiment_result_loader import ExperimentResultLoader
from bob.gradiant.core.classes.evaluation.data.pad.scores_organizer import ScoresOrganizer
from bob.gradiant.core.classes.evaluation.data.performance_extractor import PerformanceExtractor

tree = lambda: collections.defaultdict(tree)
class PadEvaluator(object):

    @staticmethod
    def run(dict_path_experiment_results, dict_metrics):

        dict_pad_data = {}
        for subsets, base_path in dict_path_experiment_results.iteritems():
            list_experiment_result = ExperimentResultLoader.load_from_folder(base_path)
            dict_pad_data[subsets] = ScoresOrganizer.run(list_experiment_result)

        dict_performance = tree()
        subset_data = dict_pad_data['Dev']
        subset = 'Dev'
        list_metrics = dict_metrics['Dev']
        for parameters in subset_data.parameters_grid:
            score_container = PadEvaluator.get_score_container_filtered_by_parameters(parameters, subset_data.list_pad_data)

            if score_container.is_empty():
                continue
            performance_from_metrics = PadEvaluator.calculate_performance(score_container, list_metrics)
            dict_performance[subset][parameters['type_attack']][parameters['framerate']][
                parameters['time_capture']] = performance_from_metrics


        if dict_pad_data.get('Test') is None:
            return dict_performance
        subset_data = dict_pad_data['Test']
        subset = 'Test'
        list_metrics_test = dict_metrics['Test']
        list_metrics_threshold = [metric.split("@")[-1] for metric in list_metrics_test]
        indices = [len(metric.split("@")) == 1 for metric in list_metrics_test]
        for i, value in enumerate(indices):
            if value == True:
                list_metrics_threshold[i] = None


        for parameters in subset_data.parameters_grid:
            score_container = PadEvaluator.get_score_container_filtered_by_parameters(parameters, subset_data.list_pad_data)
            if score_container.is_empty():
                continue
            if set([metric for metric in list_metrics_threshold if metric is not None]).issubset(list_metrics)==False:
                raise TypeError("Reference threshold has not been calculated")

            threshold = PadEvaluator.retrieve_threshold(dict_performance, parameters, list_metrics_threshold)

            performance_from_metrics = PadEvaluator.calculate_performance(score_container, list_metrics_test, threshold)
            dict_performance[subset][parameters['type_attack']][parameters['framerate']][
                parameters['time_capture']] = performance_from_metrics

        dict_performance_visualization = PadEvaluator.rearrange_dict_performance_for_visualization(dict_performance,
                                                                                                   list_metrics + list_metrics_test)
        return dict_performance_visualization

    @staticmethod
    def get_score_container_filtered_by_parameters(parameters, list_pad_data):
        list_pad_data = [pad_data for pad_data in list_pad_data if
                         pad_data.pad_info.framerate == parameters['framerate'] and
                         pad_data.pad_info.time_capture == parameters['time_capture'] and
                         pad_data.pad_info.type_attacks == parameters['type_attack']]

        if len(list_pad_data) != 1:
            raise ValueError('It must exist only one PadData following a specific parameters configuration')

        return list_pad_data[0].scores_container

    @staticmethod
    def calculate_performance(score_container, list_metrics, list_thresholds=None):

        performance_from_metric = {}
        ind_metric = 0
        for metric in list_metrics:
            if list_thresholds is None:
                threshold = None
            else:
                threshold = list_thresholds[ind_metric]
            performance_from_metric[metric] = PerformanceExtractor.run(metric.split("@")[0], score_container, threshold)
            ind_metric = ind_metric + 1
        return performance_from_metric

    @staticmethod
    def rearrange_dict_performance_for_visualization(dict_performance, list_metrics_dummy):
        dict_performance_visualization = tree()
        for subset in dict_performance.keys():
            for type_attack in dict_performance[subset].keys():
                for framerate in dict_performance[subset][type_attack].keys():
                    for time_capture in dict_performance[subset][type_attack][framerate].keys():
                        for metric in list_metrics_dummy:
                            if metric not in dict_performance[subset][type_attack][framerate][time_capture].keys():
                                continue
                            dict_performance_visualization[subset][type_attack][metric][framerate][time_capture] = \
                                dict_performance[subset][type_attack][framerate][time_capture][metric]
        fact = lambda x: 1 if x == 0 else x * fact(x - 1)
        dict_performance_visualization = PadEvaluator.default_to_regular(dict_performance_visualization)
        return dict_performance_visualization

    @staticmethod
    def default_to_regular(d):
        if isinstance(d, collections.defaultdict):
            d = {k: PadEvaluator.default_to_regular(v) for k, v in d.iteritems()}
        return d

    @staticmethod
    def retrieve_threshold(dict_performance, parameters, list_metric_threshold):
        threshold = []
        for metric in list_metric_threshold:
            if metric is not None:
                threshold.append(dict_performance['Dev'][parameters['type_attack']][parameters['framerate']]
                         [parameters['time_capture']][metric]['threshold'])
            else:
                threshold.append(None)
        return threshold


