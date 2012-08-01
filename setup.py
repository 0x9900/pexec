#!/usr/bin/env python
"""
Setup script.
"""
from distutils.core import setup


__author__ = 'Fred Cirera'


def ReadMe():
    open('README').read()


setup(name = "pexec",
      version = "0.1.0",
      description = "pexec execute several jobs in parallel",
      long_description = ReadMe(),
      author = __author__,
      author_email = 'github-fred@hidzz.com',
      license = "PSF",
      package_dir = {'pexec': 'src'},
      packages = ['pexec'],
      scripts = ['pexec'],
)
