import unittest

import numpy as np
from bob.gradiant.core import PadVisualizationManager
from bob.gradiant.core.test.test_utils import TestUtils

class UnitTestVisualization(unittest.TestCase):

    def test_create_no_dict_performance(self):
        try:
            PadVisualizationManager()
        except IOError or TypeError:
            self.assertTrue(True, "Failed test_class_create: no data")

    def test_visualization_manager(self):

        name_dataset = "OULU"
        name_algorithm = "stb"
        date = "2017/09/08 - 16:26:15"

        subset_list = ["dev"]  # , "test"]
        n_samples = 10
        attack_list = ['print', 'replay']
        metric_list = ['EER', 'FAR01']
        fps_list = np.array([5, 10, 15])
        tcapture_list = np.zeros([fps_list.size, n_samples])

        metric_value = np.zeros([attack_list.__len__(), metric_list.__len__(), fps_list.size, n_samples])

        metric_value[0, 0, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 0, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 0, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 0, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 0, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 0, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)

        metric_value[0, 1, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 1, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[0, 1, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 1, 0, :] = np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 1, 1, :] = 2 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)
        metric_value[1, 1, 2, :] = 3 * np.exp(-np.linspace(1, 10, n_samples)) + np.random.normal(0, 0.01, n_samples)

        tcapture_list[0, :] = np.linspace(1, 3 * fps_list[0], n_samples) / float(fps_list[0]) * 1000
        tcapture_list[1, :] = np.linspace(1, 3 * fps_list[1], n_samples) / float(fps_list[1]) * 1000
        tcapture_list[2, :] = np.linspace(1, 3 * fps_list[2], n_samples) / float(fps_list[2]) * 1000

        dict_performance = {}
        for i, subset in enumerate(subset_list):  # subset
            dict_performance[subset] = {}
            for j, attack in enumerate(attack_list):  # attacks
                dict_performance[subset][attack] = {}
                for k, metric in enumerate(metric_list):  # metric
                    dict_performance[subset][attack][metric] = {}
                    for l, fps in enumerate(fps_list):  # fps
                        dict_performance[subset][attack][metric][fps] = {}
                        for m in range(n_samples):
                            dict_performance[subset][attack][metric][fps][tcapture_list[l, m]] = {}
                            dict_performance[subset][attack][metric][fps][tcapture_list[l, m]]['value'] = metric_value[j,k,l,m]
                            dict_performance[subset][attack][metric][fps][tcapture_list[l, m]]['threshold'] = 0.1

        vis = PadVisualizationManager(name_dataset, name_algorithm, date, dict_performance, TestUtils.get_result_path())
        vis.plot_fig_pad_time()
        vis.plot_table()

        for i, attack in enumerate(attack_list):
            self.assertTrue(dict_performance[subset_list[0]][attack].keys().__len__() == 2)
            for j, metric in enumerate(metric_list):
                self.assertTrue(dict_performance[subset][attack][metric].keys().__len__() == 3)
                for k, fps in enumerate(fps_list):
                    self.assertTrue(dict_performance[subset][attack][metric][fps].keys().__len__() == 10)


    def test_visualization_manager_end2end(self):
        date = "16/09/2017"
        items = ["ATTACK", "NO_ATTACK"]
        name_dataset = "OULU"
        name_processor = "intel i7"
        fps = 5
        tcap = 2000
        n_pad = 150
        labels = []
        labels_true = []
        for i in range(n_pad):
            if i <= n_pad * 0.7:
                labels_true.append(items[0])
            else:
                labels_true.append(items[1])

            rnd = np.random.random((1,))
            if rnd > 0.5:
                labels.append(items[0])
            else:
                labels.append(items[1])

        dict_performance = {}
        dict_performance["processor"] = name_processor
        dict_performance["framerate"] = fps
        dict_performance["total_time_of_acquisition"] = tcap
        dict_performance["processed_frames"] = 10
        dict_performance["cpu_time_list"] = 0.5 * tcap * np.random.random_sample((n_pad,))
        dict_performance["time_of_delay_list"] = 1000.0 * np.random.random_sample((n_pad,))
        dict_performance["scores_list"] = np.random.random_sample((n_pad,))
        dict_performance["labels_list"] = labels
        dict_performance["benchmark_labels_list"] = labels_true

        pad_visualization_manager = PadVisualizationManager(name_dataset, "end2end", date, dict_performance, TestUtils.get_result_path())
        pad_visualization_manager.plot_table_end2end()



if __name__ == '__main__':
    unittest.main()
