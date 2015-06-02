#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of whoson.
# https://github.com/heynemann/whos-on-server

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Bernardo Heynemann <heynemann@gmail.com>

from setuptools import setup, find_packages
from whoson import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='whoson',
    version=__version__,
    description="Server for the who's on plugin.",
    long_description='''
Server for the who's on plugin.
''',
    keywords='realtime web',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='https://github.com/heynemann/whos-on-server',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'cow-framework',
        'tornado>3.2,<4.0',
        'tornado-redis-sentinel',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            'whoson=whoson.server:main',
        ],
    },
)
