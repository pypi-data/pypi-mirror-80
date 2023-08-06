#!/usr/bin/env python
from distutils.core import setup

description = 'CC library for python3'
keywords = ['clustering']

setup(
    name='BootstrapCCpy',
    version='0.1.1',
    description=description,
    author='FB, NN, EF, PP',
    package_data={'': ['Readme.md']},
    license="MIT",
    install_requires=[
        'numpy',
        'joblib',
        'kneed',
        'matplotlib',
        'scipy'
    ],
    url='https://github.com/NNelo/BootstrapCCpy',
    download_url='https://github.com/NNelo/BootstrapCCpy/archive/master.zip',
    keywords=keywords
)
