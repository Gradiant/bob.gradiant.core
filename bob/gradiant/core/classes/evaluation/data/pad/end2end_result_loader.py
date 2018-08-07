import os
from glob import glob
import pickle

class End2endResultLoader():
    @staticmethod
    def pickle_load(my_pickle):
        with open(my_pickle, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def load_from_folder(base_path):
        if not os.path.isdir(base_path):
            raise IOError('base_path is not a dir')

        list_filenames = [y for x in os.walk(base_path) for y in glob(os.path.join(x[0], '*.pkl'))]
        if not list_filenames:
            raise IOError('No pickle files in ', base_path)

        dict_performance = {'end2end':{}}
        for filename in list_filenames:
            path_filename = os.path.join(base_path, filename)
            subset_dict = End2endResultLoader.pickle_load(path_filename)
            dict_performance['end2end'].update(subset_dict['end2end'])
        return dict_performance