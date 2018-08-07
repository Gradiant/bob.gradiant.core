import numpy as np
import os
import unittest
import shutil

from bob.gradiant.core import PipelineFeaturesFormatLoader, FeaturesSaver
from bob.gradiant.core.test.test_utils import TestUtils


class TestPipelineFeaturesFormatLoader(unittest.TestCase):
    def setUp(self):
        self.result_path = TestUtils.get_result_path()
        self.my_dict = {'3457987645': np.array([1, 2, 3]),
                        '5678765665': np.array([10, 20, 30]),
                        '9876578765': np.array([4, 5, 6]),
                        '1235784743': np.array([40, 50, 60]),
                        '5676645675': np.array([6, 5, 3]),
                        '0756664765': np.array([1, 1, 1])}
        features_saver = FeaturesSaver(self.result_path)
        features_saver.save('grad_001_real_00_00', self.my_dict)
        features_saver.save('grad_002_attack_02_00', self.my_dict)
        features_saver.save('grad_003_real_00_00', self.my_dict)

        self.dict_labeled_basename = {'Train': {'grad_001_real_00_00': 0,
                                                'grad_002_attack_02_00': 1,
                                                'grad_003_real_00_00': 0}}

    def tearDown(self):
        if os.path.isdir(self.result_path):
            shutil.rmtree(self.result_path)

    def test_run_with_wrong_path(self):
        self.assertRaises(IOError,
                          lambda: PipelineFeaturesFormatLoader.run('wrong_path', self.dict_labeled_basename)
                          )

    def test_run_with_empty_dict_labeled_basename(self):
        self.assertRaises(ValueError,
                          lambda: PipelineFeaturesFormatLoader.run(TestUtils.get_resources_path(), dict())
                          )

    def test_run_with_none_dict_labeled_basename(self):
        self.assertRaises(ValueError,
                          lambda: PipelineFeaturesFormatLoader.run(TestUtils.get_resources_path(), None)
                          )

    def test_output_dict_shape_OK(self):
        dict_pipeline_features_format = PipelineFeaturesFormatLoader.run(self.result_path, self.dict_labeled_basename)
        self.assertEqual((18, 3), dict_pipeline_features_format['Train']['features'].shape)
        self.assertEqual((18,), dict_pipeline_features_format['Train']['keyframes'].shape)
        self.assertEqual((18,), dict_pipeline_features_format['Train']['labels'].shape)
