#!usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: setup.py
"""
DOMAuto setup script.
"""

from setuptools import setup, find_packages

PACKAGE_NAME = 'domauto'
URL = 'https://git.km3net.de/jseneca/dom_autopsy'
DESCRIPTION = 'The domauto project. Automatic DOM status plotting and autopsy'
__author__ = 'Jordan Seneca'
__email__ = 'jseneca@km3net.de'

with open('requirements-dev.txt') as fobj:
    REQUIREMENTS = [l.strip() for l in fobj.readlines()]

setup(
    name=PACKAGE_NAME,
    url=URL,
    description= DESCRIPTION,
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    setup_requires=[ 'setuptools_scm', 'wheel' ],
    use_scm_version=True,
    install_requires=REQUIREMENTS,
    python_requires='>=3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
    ],
    entry_points = {
        'console_scripts': ['domauto=src.command_line:main'],
        },
    test_suite='nose.collector',
    tests_require=['nose'],
)
