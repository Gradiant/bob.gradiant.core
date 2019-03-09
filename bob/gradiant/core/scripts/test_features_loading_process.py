import os
import numpy as np
import h5py
import shutil
import time

from bob.gradiant.core import FeaturesSaver
from bob.gradiant.core import PipelineFeaturesFormatLoader

SIZE_FEATURES = 200
N_FILES = 16000


def create_fake_n_files(path):
    for n in range(N_FILES):
        access_name = 'access_{}'.format(n)
        filename = os.path.join(path, '{}.h5'.format(access_name))
        file_root = h5py.File(filename, 'w')
        file_root.create_dataset(access_name, data=np.ones(SIZE_FEATURES))
        file_root.close()


def create_fake_1_file_with_n_acces(path):
    filename = os.path.join(path, '{}.h5'.format('all_access'))
    file_root = h5py.File(filename, 'w')
    for n in range(N_FILES):
        access_name = 'access_{}'.format(n)
        file_root.create_dataset(access_name, data=np.ones(SIZE_FEATURES))
    file_root.close()


def create_fake_database():
    print('Creating fake database...')
    path = 'result/tmp/fake_features'
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)

    create_fake_n_files(path)
    create_fake_1_file_with_n_acces(path)

    return path


def create_dummy_real_database():
    print('Creating dummy database...')
    path = 'result/tmp/dummy_features'
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)

    features_saver = FeaturesSaver(path)
    for n in range(N_FILES):
        access_name = 'access_{}'.format(n)
        my_dict = {access_name: np.ones(SIZE_FEATURES)}
        features_saver.save(access_name, my_dict)

    dict_train = {}
    for n in range(N_FILES):
        access_name = 'access_{}'.format(n)
        dict_train[access_name] = {'user': 1,
                                   'pai': 0,
                                   'common_pai': 0,
                                   'capture_device': 3,
                                   'common_capture_device': 0,
                                   'scenario': 3,
                                   'light': 1}
    dict_labeled_basename = {'Train': dict_train}

    return path, dict_labeled_basename


def print_info():
    print('size features: ' + str(SIZE_FEATURES))
    print('number files:  ' + str(N_FILES))


class Loader:
    def __init__(self):
        pass

    @staticmethod
    def run(filename_list):
        dict_features = {}
        for filename in filename_list:
            try:
                file_root = h5py.File(filename, 'r')
                for key in file_root:
                    dict_features[key] = file_root[key][:]
                file_root.close()
            except:
                raise IOError('{} impossible to read'.format(filename))
        return dict_features


def check_time_sequential_loader(name, filename_list):
    start = time.time()
    dict_features = Loader.run(filename_list)
    end = time.time()
    time_str = '{0:.4g}'.format(float(end - start))
    print('{} -> elapsed time {} s, to load {} features ({}-length)'.format(name, time_str, len(dict_features), len(
        dict_features[list(dict_features)[0]])))


def check_time_pipeline_format_loader(name, path, dict_labeled_basename):
    start = time.time()
    dict_features = PipelineFeaturesFormatLoader.run(path, dict_labeled_basename)
    end = time.time()
    time_str = '{0:.4g}'.format(float(end - start))

    print('{} -> elapsed time {} s, to load {} features ({}-length)'.format(name, time_str,
                                                                            len(dict_features['Train']['features']),
                                                                            len(dict_features['Train']['features'][0])))


def get_list_n_files(path):
    list_n_files = []
    for n in range(N_FILES):
        list_n_files.append(os.path.join(path, '{}.h5'.format('access_{}'.format(n))))
    return list_n_files


def get_list_1_file(path):
    return [os.path.join(path, 'all_access.h5')]


def delete_tmp_features(list_paths):
    for path in list_paths:
        if os.path.isdir(path):
            shutil.rmtree(path)


def main():
    path_fake_database = create_fake_database()
    path_dummy_database, dict_labeled_basename = create_dummy_real_database()

    print_info()

    check_time_sequential_loader('Load {} files'.format(N_FILES), get_list_n_files(path_fake_database))
    check_time_sequential_loader('Load 1 file{}'.format(' ' * (len(str(N_FILES)))), get_list_1_file(path_fake_database))
    check_time_pipeline_format_loader('Load from PipelineFeaturesFormatLoader',
                                      path_dummy_database,
                                      dict_labeled_basename)

    delete_tmp_features([path_fake_database, path_dummy_database])


if __name__ == '__main__':
    main()
