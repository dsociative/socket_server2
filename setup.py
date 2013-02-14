#!/usr/bin/env python

from setuptools import setup

setup(name='socket server2',
      description='socket server for flash client',
      author='dsociative',
      author_email='admin@geektech.ru',
      packages=['socket_server', 'socket_server.base',
                'socket_server.ext', 'socket_server.util',
                'socket_server.client'],
      install_requires=['pyamf', 'unittest2', 'import_file']
)
