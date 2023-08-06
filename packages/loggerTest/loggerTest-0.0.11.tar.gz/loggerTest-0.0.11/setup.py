#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 21-06-2020 12:32:28
"""
__author__ = "lairuilin"
__email__ = "kalai850531@g.ncu.edu.tw"
__status__ = "Development"

import setuptools

setuptools.setup(name='loggerTest',
      version='0.0.11',
      description='課前測試版本',
      url='https://github.com/lairuilin/logger_test',
      author='lairuilin',
      author_email='kalai850531@g.ncu.edu.tw',
      license='MIT',
      packages=['loggerTest'],
      install_requires=['jupyter'],
      include_package_data=True
     )