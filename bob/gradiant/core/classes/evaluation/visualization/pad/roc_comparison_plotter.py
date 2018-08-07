#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

import os

from bob.gradiant.core.classes.evaluation.visualization import Plotter
import matplotlib
if "BUILD_NUMBER" in os.environ: #Use agg mode on jenkins builds
    matplotlib.use('agg')
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save
from bokeh.palettes import viridis
from bokeh.models import HoverTool, Label, Range1d
import time
import numpy as np
import bob.measure


BOKEH_MARKERS = ["circle", "square", "triangle", "asterisk", "inverted_triangle", "x", "circle_x", "diamond", "cross",
                 "square_x", "circle_cross", "square_cross"]
PLT_MARKERS = ["o", "s", "^", "*", "v", "x", "D", "+", "p", "H", "|", "2"]

class RocComparisonPlotter(Plotter):
    dict_performance = None

    def __init__(self, name_database, name_algorithm, dict_performance, result_path):
        super(RocComparisonPlotter, self).__init__(name_database, name_algorithm, dict_performance, result_path)

    def run(self):

        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

        date_str = time.strftime("%Y/%m/%d") + " - " + time.strftime("%H:%M:%S")

        # plot one figure for every subset-attack-metric
        for i, subset in enumerate(self.dict_performance.keys()):
            setting_str1 = "Dataset: " + self.name_database + "   --   Compared Methods: " + str(
                self.dict_performance[subset].keys())
            setting_str2 = "Date: " + date_str
            # plot comparative of methods using FAR-FRR curve
            if subset is "end2end":

                len_subset_keys = len(self.dict_performance[subset].keys())
                curve_color = viridis(len_subset_keys)
                line_marker_bokeh = BOKEH_MARKERS[:len_subset_keys]
                line_marker_plt = PLT_MARKERS[:len_subset_keys]

                # bokeh properties setting
                hover = HoverTool(tooltips=[
                    ("index", "$index"),
                    ("FRR", "($y)"),
                    ("FAR", "($x)"), ])

                fig_bokeh = figure(plot_width=600, plot_height=500, tools=[hover, 'pan', 'wheel_zoom', 'box_zoom',
                                                                          'reset'], toolbar_location="right")
                fig_bokeh.title.text = "ROC curve. Comparative of methods"
                fig_bokeh.xaxis.axis_label = "FAR"
                fig_bokeh.yaxis.axis_label = "FRR"
                fig_bokeh.grid.grid_line_alpha = 0.3

                fig_plt, ax_plt = plt.subplots()

                n_roc_points = 25

                for j, algorithm in enumerate(self.dict_performance[subset].keys()):
                    scores_list = self.dict_performance[subset][algorithm]["scores_list"]
                    benchmark_labels_list = self.dict_performance[subset][algorithm]["benchmark_labels_list"]

                    genuine_score = [scores_list[i] for i, s in enumerate(benchmark_labels_list) if s == "NO_ATTACK"]
                    impostor_score = [scores_list[i] for i, s in enumerate(benchmark_labels_list) if s == "ATTACK"]

                    roc_far = np.zeros(n_roc_points)
                    roc_frr = np.zeros(n_roc_points)
                    for n, far in enumerate(np.linspace(0.0, 1.0, n_roc_points)):
                        threshold_far = bob.measure.far_threshold(impostor_score, genuine_score, far)
                        far, frr = bob.measure.farfrr(impostor_score, genuine_score, threshold_far)
                        roc_far[n] = far
                        roc_frr[n] = frr

                    fig_bokeh.line(roc_far, roc_frr, color=curve_color[j], legend=algorithm, line_width=2)
                    fig_bokeh.scatter(roc_far, roc_frr, size=8, marker=line_marker_bokeh[j], fill_color="white",
                                     fill_alpha=0.6, line_color=curve_color[j], legend=algorithm)
                    ax_plt.plot(roc_far, roc_frr, linewidth=2, label=algorithm, marker=line_marker_plt[j],
                               markerfacecolor="None", markersize=6)

                fig_bokeh.x_range = Range1d(start=0, end=1)
                fig_bokeh.y_range = Range1d(start=0, end=1)

                caption1 = Label(x=0, y=-15, x_units='screen', y_units='screen', text=setting_str1, render_mode='css',
                                 level="overlay", text_align="left")
                caption2 = Label(x=0, y=-15, x_units='screen', y_units='screen', text=setting_str2, render_mode='css',
                                 level="overlay", text_align="left")
                fig_bokeh.add_layout(caption1, 'below')
                fig_bokeh.add_layout(caption2, 'below')

                # Bokeh: output to static HTML file
                fig_bokeh.legend.click_policy = "hide"

                path = os.path.join(self.result_path, self.name_database + "_end2end_ROC_figure.html")
                output_file(path)
                save(fig_bokeh)

                # matplotlib: properties setting
                ax_plt.grid(True)
                ax_plt.legend(loc='upper right')
                ax_plt.set_title("ROC curve. Comparative of methods")
                ax_plt.set_xlabel("FAR")
                ax_plt.set_ylabel("FRR")
                path = os.path.join(self.result_path, self.name_database + "_end2end_ROC_figure.png")
                fig_plt.savefig(path, bbox_inches='tight')


                continue