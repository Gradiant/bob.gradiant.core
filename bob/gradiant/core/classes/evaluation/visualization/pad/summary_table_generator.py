#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

import os
import pandas as pd
import numpy as np
from bob.gradiant.core.classes.evaluation.visualization.table_generator import TableGenerator
from bob.gradiant.core.classes.evaluation.data.pad.summary_performance_result import SummaryPerformanceResult

METRICS_EVALUATION = ['EER', 'HTER@EER', 'ACER@EER', 'APCER@EER', 'BPCER@EER']


def highlight_max(data, color='yellow'):
    """
    highlight the maximum in a Series or DataFrame
    """
    attr = 'background-color: {}'.format(color)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)


class SummaryTableGenerator(TableGenerator):
    dict_performance = None

    def __init__(self, name_database, name_algorithm, dict_performance, result_path):
        super(SummaryTableGenerator, self).__init__(name_database, name_algorithm, dict_performance, result_path)

    def get_dict_all_configurations(self, dict_attacks):
        dict_all_configurations = {}

        for key_metric, dict_metrics in dict_attacks.items():
            for key_framerate, dict_framerate in dict_metrics.items():
                for key_time_capture, dict_time_capture in dict_framerate.items():
                    configuration = self.get_configuration_name(key_framerate, key_time_capture)
                    dict_all_configurations[configuration] = (key_framerate, key_time_capture)
        return dict_all_configurations

    def get_configuration_name(self, key_framerate, key_time_capture):
        configuration_name = 'default'
        if key_framerate != 30 or key_time_capture != -1:
            configuration_name = 'fps_' + str(key_framerate) + '_tc_' + str(int(key_time_capture))
        return configuration_name

    def check_list_metrics(self, list_metrics):
        if not all(metric in METRICS_EVALUATION for metric in list_metrics):
            raise IOError(
                'SummaryTableGenerator need [' + str(METRICS_EVALUATION) + '] metric to generate the report table')

    def get_dict_metrics_from_tuple_configuration(self, dict_attack, tuple_configuration):

        key_framerate = tuple_configuration[0]
        key_time_capture = tuple_configuration[1]
        dict_metrics = {}
        for metric in dict_attack:
            dict_metrics[metric] = dict_attack[metric][key_framerate][key_time_capture]['value']
        return dict_metrics

    def get_dict_thresholds_from_tuple_configuration(self, dict_attack, tuple_configuration):

        key_framerate = tuple_configuration[0]
        key_time_capture = tuple_configuration[1]

        dict_thresholds = {}
        for metric in dict_attack:
                dict_thresholds[metric] = dict_attack[metric][key_framerate][key_time_capture]['threshold']
        return dict_thresholds

    def run(self):
        list_summary_performance_result = []
        th_dev = 0.0
        eer_dev = 0.0

        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

        for key_subset, dict_subsets in self.dict_performance.items():
            for key_attack, dict_attacks in dict_subsets.items():

                list_metrics = list(dict_attacks)
                self.check_list_metrics(list_metrics)

                dict_all_configurations = self.get_dict_all_configurations(dict_attacks)
                if key_attack == 'all_attacks':
                    for configuration, tuple_configuration in dict_all_configurations.items():
                        dict_metrics = self.get_dict_metrics_from_tuple_configuration(dict_attacks,
                                                                                      tuple_configuration)
                        dict_thresholds = self.get_dict_thresholds_from_tuple_configuration(dict_attacks,
                                                                                            tuple_configuration)
                        if key_subset == 'Dev':
                            th_dev = dict_thresholds['EER']
                            eer_dev = dict_metrics['EER']

                        else:
                            summary_performance_result = SummaryPerformanceResult(self.name_database,
                                                                                  self.name_algorithm,
                                                                                  configuration,
                                                                                  th_dev,
                                                                                  eer_dev,
                                                                                  dict_metrics['HTER@EER'],
                                                                                  dict_metrics['ACER@EER'],
                                                                                  dict_metrics['APCER@EER'],
                                                                                  dict_metrics['BPCER@EER'])
                            list_summary_performance_result.append(summary_performance_result)

                    # table for subset and kind of attack
                    list_configurations = [summary_performance_result.configuration for summary_performance_result in
                                           list_summary_performance_result]
                    list_eer_dev = [summary_performance_result.eer_dev for summary_performance_result in
                                    list_summary_performance_result]
                    list_threshold_dev = [summary_performance_result.threshold_dev for summary_performance_result in
                                          list_summary_performance_result]
                    list_hter = [summary_performance_result.hter for summary_performance_result in
                                 list_summary_performance_result]
                    list_acer = [summary_performance_result.acer for summary_performance_result in
                                 list_summary_performance_result]
                    list_apcer = [summary_performance_result.apcer for summary_performance_result in
                                  list_summary_performance_result]
                    list_bpcer = [summary_performance_result.bpcer for summary_performance_result in
                                  list_summary_performance_result]

                    data_frame = pd.DataFrame({'Database': self.name_database,
                                               'Algorithm': self.name_algorithm,
                                               'Configuration': pd.Categorical(list_configurations),
                                               'EER@Dev': pd.Series(list_eer_dev),
                                               'Th@Dev': pd.Series(list_threshold_dev),
                                               'HTER@EER': pd.Series(list_hter),
                                               'ACER@EER': pd.Series(list_acer),
                                               'APCER@EER': pd.Series(list_apcer),
                                               'BPCER@EER': pd.Series(list_bpcer),
                                               })
                    data_frame = data_frame[
                        ['Database', 'Algorithm', 'Configuration', 'EER@Dev', 'Th@Dev', 'HTER@EER', 'ACER@EER',
                         'APCER@EER', 'BPCER@EER']]
                    data_frame = data_frame.sort_values(['ACER@EER'], ascending=[True])

                    filename = '_'.join([self.name_database, key_attack, 'summary_table'])

                    data_frame.to_html(os.path.join(self.result_path, filename + '.html'))
                    data_frame.to_latex(os.path.join(self.result_path, filename + '.tex'))
                    data_frame.to_csv(os.path.join(self.result_path, filename + '.csv'))
