#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='socket server2',
      description='socket server for flash client',
      author='dsociative',
      author_email='admin@geektech.ru',
      packages=find_packages(),
      install_requires=['unittest2', 'import_file']
)
