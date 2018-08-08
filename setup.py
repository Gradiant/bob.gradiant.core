#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2018+ Gradiant, Vigo, Spain

from setuptools import setup, find_packages
from version import *

setup(
    name='bob.gradiant.core',
    version=get_version(),
    description='Python package which defines useful rules and interfaces for biometrics researching',
    url='http://pypi.python.org/pypi/template-gradiant-python',
    license='BSD-3',
    author='Biometrics Team (Gradiant)',
    author_email='biometrics.support@gradiant.org',
    long_description=open('README.md').read(),
    keywords='template gradiant',

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,

    install_requires=[
      "setuptools",
    ],

    entry_points={
      'console_scripts': [
        'test_features_loading_process.py = bob.gradiant.core.scripts.test_features_loading_process:main',
      ],
    },
)
