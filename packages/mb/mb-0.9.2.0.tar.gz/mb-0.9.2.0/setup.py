#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

setup_requirements = [ 'youtube-dl','requests','pydub','sh']

test_requirements = [ ]

setup(
    description="temp",
    install_requires=requirements,
    include_package_data=True,
    name='mb',
    packages=['mb'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    version='0.9.2.0',
    zip_safe=False,
)
