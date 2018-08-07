#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

import os
from bob.gradiant.core.classes.evaluation.visualization.pad.end_to_end_table_generator import EndToEndTableGenerator
from bob.gradiant.core.classes.evaluation.visualization.pad.roc_comparison_plotter import RocComparisonPlotter
from bob.gradiant.core.classes.evaluation.visualization.pad.summary_table_generator import SummaryTableGenerator
from bob.gradiant.core.classes.evaluation.visualization.pad.framerate_and_time_comparison_table_generator import \
    FramerateAndTimeComparisonTableGenerator
from bob.gradiant.core.classes.evaluation.visualization.pad.framerate_and_time_comparison_plotter import \
    FramerateAndTimeComparisonPlotter

class PadVisualizationManager:
    def __init__(self, name_database=None, name_algorithm=None, date=None, dict_performance=None, store_path='.'):
        self.asssert_input(date, dict_performance, name_algorithm, name_database, store_path)
        self.name_database = name_database
        self.name_algorithm = name_algorithm
        self.date = date
        self.store_path = store_path
        self.dict_performance = dict_performance

        self.list_plotters = [FramerateAndTimeComparisonPlotter(self.name_database,
                                                                self.name_algorithm,
                                                                dict_performance,
                                                                os.path.join(store_path, 'plots',
                                                                             'framerate_and_time_comparison'))
                              ]

        self.list_table_generators = [SummaryTableGenerator(self.name_database,
                                                            self.name_algorithm,
                                                            dict_performance,
                                                            os.path.join(store_path, 'tables', 'summary')),
                                      FramerateAndTimeComparisonTableGenerator(self.name_database,
                                                                               self.name_algorithm,
                                                                               dict_performance,
                                                                               os.path.join(store_path, 'tables',
                                                                                            'framerate_and_time_comparison'))

                                      ]

    @classmethod
    def asssert_input(cls, date, dict_performance, name_algorithm, name_database, store_path):
        if dict_performance is None:
            raise IOError('dict_performance is empty')
        if not isinstance(store_path, basestring):
            raise TypeError('store_path must be a string')
        if not isinstance(name_database, basestring):
            raise TypeError('name_database must be a string')
        if not isinstance(name_algorithm, basestring):
            raise TypeError('name_algorithm must be a string')
        if not isinstance(date, basestring):
            raise TypeError('date must be a string')


    def plot_fig_pad_time(self):
        for plotter in self.list_plotters:
            try:
                plotter.run()
            except:
                continue

    def plot_table(self):
        for table_generator in self.list_table_generators:
            try:
                table_generator.run()
            except IOError:
                continue

    def plot_fig_roc_comparative_methods(self):
        plotter = RocComparisonPlotter(self.name_database,
                                          self.name_algorithm,
                                          self.dict_performance,
                                          os.path.join(self.store_path, 'end2end','roc'))
        plotter.run()


    def plot_table_end2end(self):
        table_generator = EndToEndTableGenerator(self.name_database,
                                                 self.name_algorithm,
                                                 self.dict_performance,
                                                 os.path.join(self.store_path, 'end2end','table'))
        table_generator.run()


