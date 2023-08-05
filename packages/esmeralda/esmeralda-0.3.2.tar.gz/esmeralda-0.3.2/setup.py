#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import versioneer

setup(
    name='esmeralda',
    author="doubleO8",
    author_email="wb008@hdm-stuttgart.de",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="no description",
    long_description="no long description either",
    url="https://doubleo8.github.io/esmeralda/",
    packages=['esmeralda'],
    install_requires=[
        'pendulum>=2.1.2',
        'Jinja2>=2.11.2',
        'djali>=0.1.10',
        'quasimodo>=0.6.5'
    ]
)
