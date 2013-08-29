#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" install eWRT :) """
from setuptools import setup, find_packages

from sys import exit

setup(
      ###########################################
      ## Metadata
      name="notifyTools",
      version="0.0.2",
      description='A set of tools for monitoring Web pages',
      author='Albert Weichselbraun',
      author_email='albert@weichselbraun.net',
      license="GPL3",
      package_dir={'': 'src'},

      ###########################################
      ## Run unittests
      test_suite='nose.collector',

      ###########################################
      ## Package List
      packages = find_packages('src'),

)
