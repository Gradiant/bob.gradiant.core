import unittest
import os
import numpy as np
import shutil

from bob.gradiant.core import FramerateAndTimeComparisonTableGenerator
from bob.gradiant.core.test.test_utils import TestUtils

class UnitTestFramerateAndTimeComparisonTableGenerator(unittest.TestCase):

    def setUp(self):
        self.list_extensions = ['html', 'tex', 'csv']
        self.result_path = os.path.join(TestUtils.get_result_path(),'framerate_and_time_comparison_table_generator')
        if os.path.isdir(self.result_path):
            shutil.rmtree(self.result_path)

    def test_run(self):
        name_database = "DATABASE"
        name_algorithm = "Algorithm"

        synthetic_dict_performance = TestUtils.get_synthetic_dict_performance()

        table_generator = FramerateAndTimeComparisonTableGenerator(name_database, name_algorithm, synthetic_dict_performance, self.result_path)
        table_generator.run()

        for extension in self.list_extensions:
            filename = '_'.join([name_database, 'all_attacks_comparison_table.' +extension])
            self.assertTrue(os.path.isfile(os.path.join(self.result_path, filename)))




if __name__ == '__main__':
    unittest.main()
