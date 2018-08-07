import unittest
import os
import shutil

from bob.gradiant.core import EndToEndInfo, EndToEndTableGenerator
from bob.gradiant.core.test.test_utils import TestUtils

class UnitTestEndToEndTableGenerator(unittest.TestCase):

    def setUp(self):
        self.list_extensions = ['html', 'tex', 'csv']
        self.result_path = os.path.join(TestUtils.get_result_path(),'end_to_end_table_generator')
        if os.path.isdir(self.result_path):
            shutil.rmtree(self.result_path)

    def test_run(self):
        name_database = "database_name@grandtest"

        filename = os.path.join(TestUtils.get_resources_path(), 'evaluation', 'end_to_end', 'end_to_end_info.h5')
        end_to_end_info = EndToEndInfo.fromfilename(filename)
        name_algorithm = end_to_end_info.name_algorithm
        table_generator = EndToEndTableGenerator(name_database, name_algorithm, dict(end_to_end_info), self.result_path)
        table_generator.run()

        for extension in self.list_extensions:
            name = '_'.join(['end_to_end_table_generator.' +extension])
            filename = os.path.join(self.result_path, name)
            self.assertTrue(filename)


if __name__ == '__main__':
    unittest.main()
