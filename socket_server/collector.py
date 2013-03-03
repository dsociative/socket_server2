# -*- coding: utf8 -*-
from os import walk
from os.path import join
from inspect import getmembers, isclass

from import_file import import_file
from socket_server.command import ServerCommand


class Collector(object):

    def __init__(self, path):
        self.path = path

    def files(self):
        for root, dirs, files in walk(self.path, topdown=False):
            for file in files:
                yield join(root, file)

    def python_files(self):
        for filename in self.files():
            if filename.endswith('.py'):
                yield filename

    def inmodule(self, cls, module):
        return cls.__module__ == module.__name__

    def iscommand(self, cls):
        return issubclass(cls, ServerCommand)

    def classes(self):
        for path in self.python_files():
            module = import_file(path)
            for name, cls in getmembers(module, isclass):
                if self.inmodule(cls, module):
                    yield cls

    def commands(self):
        for cls in self.classes():
            if self.iscommand(cls):
                yield cls

    def mapper_gen(self):
        for command in self.commands():
            yield command.name, command

    def mapper(self):
        return dict(self.mapper_gen())