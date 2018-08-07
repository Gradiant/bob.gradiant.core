#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

import os
from bob.gradiant.core.classes.evaluation.visualization.plotter import Plotter
import matplotlib
if "BUILD_NUMBER" in os.environ: #Use agg mode on jenkins builds
    matplotlib.use('agg')
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save
from bokeh.palettes import viridis
from bokeh.models import HoverTool, Label, Range1d
import time
import numpy as np

BOKEH_MARKERS = ["circle", "square", "triangle", "asterisk", "inverted_triangle", "x", "circle_x", "diamond", "cross",
                 "square_x", "circle_cross", "square_cross"]
PLT_MARKERS = ["o", "s", "^", "*", "v", "x", "D", "+", "p", "H", "|", "2"]

class FramerateAndTimeComparisonPlotter(Plotter):
    dict_performance = None

    def __init__(self, name_database, name_algorithm, dict_performance, result_path):
        super(FramerateAndTimeComparisonPlotter, self).__init__(name_database, name_algorithm, dict_performance, result_path)

    def run(self):

        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

        date_str = time.strftime("%Y/%m/%d") + " - " + time.strftime("%H:%M:%S")

        bokeh_store_path = self.get_store_path_from_folder(self.result_path, 'bokeh')
        matplotlib_store_path = self.get_store_path_from_folder(self.result_path, 'matplotlib')

        # plot one figure for every subset-attack-metric
        for subset in self.dict_performance.keys():
            if subset is "end2end":
                continue
            for attack in self.dict_performance[subset].keys():
                for metric in self.dict_performance[subset][attack].keys():
                    text_database_info = "Dataset: " + self.name_database + ' (' + subset + ')'
                    text_method = "Method: " + self.name_algorithm
                    text_date_info = "Date: " + date_str
                    protocol_info = "Protocol: " + attack + ' - spoofing attack'
                    text_x_label = "time capture (s)"
                    text_y_label = metric + " (%)"

                    len_metric_keys = len(self.dict_performance[subset][attack][metric].keys())
                    curve_color = viridis(len_metric_keys)
                    line_marker_bokeh = BOKEH_MARKERS[:len_metric_keys]
                    line_marker_plt = PLT_MARKERS[:len_metric_keys]

                    fig_bokeh = self.get_fig_bokeh(metric, protocol_info, text_method, text_x_label, text_y_label)
                    fig_plt, ax_plt = plt.subplots()

                    # plot one curve for every FPS rate
                    for index_fps, fps in enumerate(self.dict_performance[subset][attack][metric].keys()):
                        x_data, y_data, is_standard_evaluation, value_standard_evaluation = self.get_data(attack, fps,
                                                                                                          metric,
                                                                                                          subset)

                        fig_bokeh.line(x_data, y_data, color=curve_color[index_fps], legend="FPS=" + str(int(fps)),
                                       line_width=2)
                        fig_bokeh.scatter(x_data, y_data, size=8, marker=line_marker_bokeh[index_fps],
                                          fill_color="white",
                                          fill_alpha=0.6, line_color=curve_color[index_fps],
                                          legend="FPS=" + str(int(fps)))

                        ax_plt.plot(x_data, y_data, linewidth=2, label="FPS=" + str(int(fps)),
                                    marker=line_marker_plt[index_fps],
                                    markerfacecolor="None", markersize=6)

                        # todo: axes = ax_plt.gca(); axes.set_ylim([0, 40])


                        if is_standard_evaluation:
                            labels = ax_plt.get_xticks().tolist()
                            index = np.where(np.array(labels) == value_standard_evaluation)[0][0]
                            labels[index] = 'Whole video'
                            ax_plt.set_xticklabels(labels)

                    caption1 = Label(x=0, y=-15, x_units='screen', y_units='screen', text=text_database_info,
                                     render_mode='css', level="overlay", text_align="left")
                    caption2 = Label(x=0, y=-15, x_units='screen', y_units='screen', text=text_date_info,
                                     render_mode='css', level="overlay", text_align="left")

                    fig_bokeh.x_range = Range1d(start=0, end=3)

                    fig_bokeh.add_layout(caption1, 'below')
                    fig_bokeh.add_layout(caption2, 'below')

                    # Bokeh: output to static HTML file
                    fig_bokeh.legend.click_policy = "hide"

                    path = os.path.join(bokeh_store_path,
                                            self.name_database + "_" + attack + "_" + metric + "_figure.html")
                    output_file(path)
                    save(fig_bokeh)

                    # todo: solve problem with the version of the phantomjs package (maybe it is solved using > v2.0) to export png images using bokeh
                    # export_png(figBokeh, filename=self.database+"_"+attack+"_"+metric+"_figure2.png")

                    # matplotlib: properties setting
                    ax_plt.grid(True)
                    ax_plt.legend(loc='upper right')
                    title_complete = '\n'.join([text_method, text_database_info, protocol_info])
                    ax_plt.set_title(title_complete)
                    ax_plt.set_xlabel(text_x_label)
                    ax_plt.set_ylabel(text_y_label)

                    path = os.path.join(matplotlib_store_path,
                                            self.name_database + "_" + attack + "_" + metric + "_figure.png")
                    fig_plt.savefig(path, bbox_inches='tight')

                    plt.close('all')

    def get_store_path_from_folder(self, base_path, folder):
        store_path = os.path.join(base_path, folder)
        if not os.path.isdir(store_path):
            os.makedirs(store_path)
        return store_path

    def get_data(self, attack, fps, metric, subset):
        list_time_capture = self.dict_performance[subset][attack][metric][fps].keys()

        value_standard_evaluation = 0
        is_standard_evaluation = False
        if -1 in list_time_capture:
            is_standard_evaluation = True
            max_value_keys = max(list_time_capture)
            if max_value_keys == -1:  # standard evaluation (whole video)
                list_time_capture = [0]
            else:
                index_standard_evaluation = np.where(np.array(list_time_capture) == -1)[0][0]
                non_standard_values = [x for x in list_time_capture if x > -1]
                if len(non_standard_values) == 1:
                    mean_diff_between_values = non_standard_values[0]
                else:
                    mean_diff_between_values = np.mean(np.diff(non_standard_values))
                value_standard_evaluation = max_value_keys + mean_diff_between_values
                list_time_capture[index_standard_evaluation] = value_standard_evaluation

        x_data = np.array(list_time_capture) / 1000.0
        sort_index = sorted(range(len(x_data)), key=lambda s: x_data[s])
        x_data.sort()
        y_aux = [np.array(self.dict_performance[subset][attack][metric][fps][x]['value']) for x in
                 self.dict_performance[subset][attack][metric][fps] if
                 self.dict_performance[subset][attack][metric][fps][x]['value'] is not None]
        y_data = [y_aux[i] for i in sort_index]
        return x_data, y_data, is_standard_evaluation, value_standard_evaluation / 1000.0

    def get_fig_bokeh(self, metric, protocol_info, text_method, text_x_label, text_y_label):
        # bokeh properties setting
        hover = HoverTool(tooltips=[
            ("index", "$index"),
            (metric, "($y)"),
            ("t_capture", "($x)"), ])
        fig_bokeh = figure(plot_width=600, plot_height=500, tools=[hover, 'pan', 'wheel_zoom', 'box_zoom',
                                                                   'reset'], toolbar_location="right")
        fig_bokeh.title.text = ' - '.join([text_method, protocol_info])
        fig_bokeh.xaxis.axis_label = text_x_label
        fig_bokeh.yaxis.axis_label = text_y_label
        fig_bokeh.grid.grid_line_alpha = 0.3
        return fig_bokeh
