#!/usr/bin/env python
from distutils.core import setup

description = 'CC library for python3'
keywords = ['clustering']

setup(
    name='BootstrapCCpy',
    version='0.1',
    description=description,
    author='FB, NN, EF, PP',
    package_data={'': ['Readme.md']},
    license="MIT",
    install_requires=[
        'numpy~=1.19.1',
        'joblib~=0.16.0',
        'kneed~=0.7.0',
        'matplotlib~=3.3.2',
        'scipy~=1.5.2'
    ],
    url='https://github.com/NNelo/BootstrapCCpy',
    download_url='https://github.com/NNelo/BootstrapCCpy/archive/master.zip',
    keywords=keywords
)
