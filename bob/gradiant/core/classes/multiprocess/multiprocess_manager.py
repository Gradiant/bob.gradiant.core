#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from joblib import Parallel, delayed


def parallel_function(object, function, args):
    funct = getattr(object, function, None)
    if callable(funct):
        return funct(*args)
    else:
        raise ValueError('Function {} is not callable.'.format(function))


class MultiprocessManager:
    """ This class is designed to parallelize a FeaturesExtractionManager (bob.gradiant.pad.protocols.classes.features_extractor.features_extractor_manager) run function.
    You can find an example in bob/gradiant/pad/protocols/scripts/parallelized_protocol_example.py where a complete dummy protocol is typed

    NOTE: As this class creates multiple python process, each process will get a copy of the arguments,
     so if your FeaturesExtractedManager needs some resources you ensure they are loaded in each run() function call or they are passed as arguments.
    """

    _n_threads = 1
    _parallel_verbose = 0

    def __init__(self, n_threads=1, options=None):
        if n_threads is not None:
            if not isinstance(n_threads, int):
                raise TypeError('Options parameter must be an integer value or None')
            self._n_threads = n_threads
        if options is not None:
            if isinstance(options, dict):
                self._options = options
                if 'verbose' in options.keys():
                    self._parallel_verbose = options['verbose']
            else:
                raise TypeError('Options parameter must be a dictionary or None')

    def run(self, object, args_list, function_to_run='run'):
        try:
            results = Parallel(n_jobs=self._n_threads, verbose=self._parallel_verbose, backend='multiprocessing')(delayed(parallel_function)(object, function_to_run, argsI) for argsI in args_list)
        except IOError as e:
            print(str(e))
            results = []
        return results

