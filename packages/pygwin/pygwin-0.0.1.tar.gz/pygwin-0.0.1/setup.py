#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

import pygwin

setup(
    name='pygwin',
    version=pygwin.VERSION,
    description='pygame window system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/qouify/pygwin/',
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    packages=find_packages('.'),
    package_dir={'': '.'},
    package_data={'pygwin.test': [os.path.join('media', '*')]},
    install_requires=[
        'pygame'
    ]
)
