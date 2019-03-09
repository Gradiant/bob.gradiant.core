import glob
import os

import h5py
import numpy as np

path = '/home/mlorenzo/Software/bob.gradiant.core/resources/evaluation/subsets_only_standard_evaluation/test'

def main():

    for root , dirs, files in os.walk(path):
        if files:
            for file in files:
                if file.endswith('.h5'):
                    hdf5_file = "{}/{}".format(root, file)
                    with h5py.File(hdf5_file, 'r+') as file_root:
                        if 'access_names' not in file_root:
                            access_names = np.repeat('video1', file_root['labels'].shape[0], axis=0)
                            file_root.create_dataset('access_names', data=access_names, dtype="S10")

                        if 'common_capture_devices' not in file_root:
                            labels = np.ones(file_root['labels'].shape, dtype=int)
                            file_root.create_dataset('common_capture_devices', data=labels)

                        if 'common_labels' in file_root:
                            labels = np.ones(file_root['labels'].shape, dtype=int)
                            del file_root['common_labels']
                            file_root.create_dataset('common_pai', data=labels)

                        if 'db_labels' not in file_root:
                            labels = np.ones((file_root['labels'].shape[0], 4), dtype=int)
                            file_root.create_dataset('db_labels', data=labels)

                        if 'devices_correspondences' not in file_root:
                            devices_correspondences = {'devices_correspondences':
                                {
                                    'device-1': 1,
                                    'device-2': 2
                                }
                            }

                            recursively_save_dict_contents_to_group(file_root, '/', devices_correspondences)


def recursively_save_dict_contents_to_group(h5file, path, dic):
    """
    ....
    """
    for key, item in dic.items():
        if isinstance(item, (np.ndarray, np.int, np.int64, np.float64, str, bytes)):
            h5file[path + key] = item
        elif isinstance(item, dict):
            recursively_save_dict_contents_to_group(h5file, path + key + '/', item)
        else:
            raise ValueError('Cannot save %s type' % type(item))


if __name__ == "__main__":
    main()
