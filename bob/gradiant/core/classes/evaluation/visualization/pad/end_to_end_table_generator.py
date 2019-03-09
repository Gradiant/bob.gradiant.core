#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from __future__ import division
import os
import numpy as np
import pandas as pd
from bob.gradiant.core.classes.evaluation.visualization.table_generator import TableGenerator


class EndToEndTableGenerator(TableGenerator):
    dict_performance = None

    def __init__(self, name_database, name_algorithm, dict_performance, result_path):
        super(EndToEndTableGenerator, self).__init__(name_database, name_algorithm, dict_performance, result_path)

    def run(self, name_algorithm='name_algorithm'):

        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

        # plot one figure for every subset-attack-metric

            # todo: create table with a comparison of methods (mean +- std) for t_response, tdelay, alpha_cpu
        table_dic = {"Method": [],
                     "Accuracy": [],
                     "Framerate": [],
                     "Time time of acquisition": [],
                     "Time response": [],
                     "Total process/CPU time": [],
                     "Process/CPU time per frame": [],
                     "CPU Usage": []
                     }

        framerate = self.dict_performance["framerate"]
        total_time_of_acquisition = self.dict_performance["total_time_of_acquisition"]
        processed_frames = np.array(self.dict_performance["processed_frames"])
        cpu_time_list = self.dict_performance["cpu_time_list"]
        time_of_delay_list = self.dict_performance["time_of_delay_list"]
        labels = np.array(self.dict_performance["labels_list"])
        benchmark_labels = np.array(self.dict_performance["benchmark_labels_list"])

        table_dic["Method"].append(name_algorithm)
        accuracy = 100.0 * np.sum(labels == benchmark_labels) / labels.size
        table_dic["Accuracy"].append(str(np.round(accuracy, 2)) + " %")
        table_dic["Framerate"].append(str(framerate) + " FPS")
        table_dic["Time time of acquisition"].append(str(round(total_time_of_acquisition / 1000.0, 2))+ " s")
        table_dic["Time response"].append(str(np.round(np.mean(np.array(time_of_delay_list)), 2)) + "+-" +
                                          str(np.round(np.std(np.array(time_of_delay_list)), 2)) + " ms")

        table_dic["Total process/CPU time"].append(str(np.round(np.mean(np.array(cpu_time_list)), 2)) + "+-" +
                                                   str(np.round(np.std(np.array(cpu_time_list)), 2)) + " ms")

        table_dic["Process/CPU time per frame"].append(str(np.round(np.mean(np.array(cpu_time_list)/np.array(processed_frames)), 2)) + "+-" +
                                                       str(np.round(np.std(np.array(cpu_time_list)/np.array(processed_frames)), 2)) + " ms")

        table_dic["CPU Usage"].append(str(round(100 * np.mean(np.array(cpu_time_list)) / total_time_of_acquisition, 2)) + " %")

        data_frame = pd.DataFrame(table_dic)

        data_frame = data_frame[
            ['Method', 'Accuracy', 'Framerate', 'Time time of acquisition', 'Time response', 'Total process/CPU time',
             'Process/CPU time per frame', 'CPU Usage']]

        # todo: pandas style is not working, check for updates!
        # table_df.style.apply(self.highlight_max, color='darkorange', subset=['t_resp (mean)', 't_resp (std)',
        # 'cpu (mean)', 'cpu (std)'])
        # table_df.style.format({'t_resp (mean)': "{:0<4.0f}", 't_resp (std)': lambda x: "+-{:.2f}".format(abs(x))})
        # table_df.style.highlight_min(subset=['t_resp (mean)', 't_resp (std)', 'cpu (mean)', 'cpu (std)'], axis=0)

        filename = '_'.join([self.name_database, '_end2end_table'])
        data_frame.to_html(os.path.join(self.result_path, filename + '.html'), bold_rows=True)
        data_frame.to_latex(os.path.join(self.result_path, filename + '.tex'), bold_rows=True)
        data_frame.to_csv(os.path.join(self.result_path, filename + '.csv'))



