#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

import os
import pandas as pd
import numpy as np
from bob.gradiant.core.classes.evaluation.visualization.table_generator import TableGenerator

class FramerateAndTimeComparisonTableGenerator(TableGenerator):
    dict_performance = None

    def __init__(self, name_database, name_algorithm, dict_performance, result_path):
        super(FramerateAndTimeComparisonTableGenerator, self).__init__(name_database, name_algorithm, dict_performance, result_path)

    def run(self):

        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

        for i, subset in enumerate(self.dict_performance.keys()):
            if subset is "end2end":
                continue
            for j, attack in enumerate(self.dict_performance[subset].keys()):
                table_dic = {}
                table_dic['WorkPoint'] = []
                table_dic['Performance@Tmax'] = []
                workpoint_lol = []  # lol means list of lists (don't get wrong)
                best_performance_lol = []

                if attack == 'all_attacks':
                    for k, metric in enumerate(self.dict_performance[subset][attack].keys()):
                        first_fps = list(self.dict_performance[subset][attack][metric].keys())[0]
                        nsamples = len(self.dict_performance[subset][attack][metric][first_fps].keys())
                        values = np.zeros([self.dict_performance[subset][attack][metric].keys().__len__(), nsamples])

                        for l, fps in enumerate(self.dict_performance[subset][attack][metric].keys()):
                            ind2sec = np.argmin(
                                np.abs(np.array(self.dict_performance[subset][attack][metric][fps].keys()) - 2000))
                            tcap4ind2sec = list(self.dict_performance[subset][attack][metric][fps].keys())[ind2sec]
                            val4ind2sec = self.dict_performance[subset][attack][metric][fps][tcap4ind2sec]['value']

                            table_dic['Performance@Tmax'].append(
                                str(round(float(val4ind2sec), 4)) + "  @FPS=" + str(int(fps)))

                            values[l, :] = [np.array(self.dict_performance[subset][attack][metric][fps][x]['value']) for x
                                            in self.dict_performance[subset][attack][metric][fps].keys()]

                        ind_min = np.argwhere(np.abs(values) == np.min(np.abs(values)))

                        fps_min = list(self.dict_performance[subset][attack][metric].keys())[ind_min[0][0]]
                        tcap_min = list(self.dict_performance[subset][attack][metric][fps].keys())[ind_min[0][1]]

                        best_perf_aux = ['-'] * self.dict_performance[subset][attack][metric].keys().__len__()
                        best_perf_aux[ind_min[0][0]] = str(round(float(values[ind_min[0][0]][ind_min[0][1]]), 4)) + \
                                                       "  @t_cap=" + str(round(float(tcap_min) / 1000.0, 2)) + "s" + \
                                                       ", FPS=" + str(fps_min)
                        best_performance_lol.append(best_perf_aux)

                        workpoint_lol_aux = ['-'] * self.dict_performance[subset][attack][metric].keys().__len__()
                        workpoint_lol_aux[0] = metric
                        workpoint_lol.append(workpoint_lol_aux)

                table_dic['BestPerformance'] = [val for sublist in best_performance_lol for val in sublist]
                table_dic['WorkPoint'] = [val for sublist in workpoint_lol for val in sublist]

                data_frame = pd.DataFrame(table_dic)
                data_frame = data_frame[['WorkPoint', 'Performance@Tmax', 'BestPerformance']]
                # table_df.set_index('WorkPoint', inplace=True)
                # table_df.fillna('-')

                filename = '_'.join([self.name_database, attack, 'comparison_table'])
                data_frame.to_html(os.path.join(self.result_path,filename + '.html'))
                data_frame.to_latex(os.path.join(self.result_path,filename + '.tex'))
                data_frame.to_csv(os.path.join(self.result_path,filename + '.csv'))


