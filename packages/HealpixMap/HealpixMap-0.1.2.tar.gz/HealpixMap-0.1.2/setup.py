#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='HealpixMap',
      version='0.1.2',
      author='Israel Martinez-Castellanos',
      author_email='imc@umd.edu',
      url='https://gitlab.com/burstcube/HealpixMap',
      packages = find_packages(include=["HealpixMap", "HealpixMap.*"]),
      install_requires = ['healpy']
      )

