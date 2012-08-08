#!/usr/bin/env python

from distutils.core import setup

setup(name='socket server2',
      description='socket server for flash client',
      author='dsociative',
      author_email='admin@geektech.ru',
      packages=['socket_server', 'socket_server.base',
                'socket_server.ext', 'socket_server.http',
                'socket_server.util'],
     )
