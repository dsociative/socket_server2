# -*- coding: utf8 -*-
from os.path import abspath, dirname, join, basename
from socket_server.collector import Collector
from socket_server.test import TestCase
from socket_server.test.ze_commands.authorization import Authorization


def names(cmds):
    return [cmd.__name__ for cmd in cmds]


def filenames(paths):
    return [basename(p) for p in paths]


class CollectorTest(TestCase):

    def setUp(self):
        path = join(abspath(dirname(__file__) + '/../ze_commands'))
        self.collector = Collector(path)

    def test_iscommand(self):
        self.assertTrue(self.collector.iscommand(Authorization))

    def test_inmodule(self):
        from socket_server.test.ze_commands import authorization
        import socket_server

        self.assertTrue(self.collector.inmodule(Authorization, authorization))
        self.assertFalse(self.collector.inmodule(Authorization, socket_server))

    def test_python_files(self):
        self.assertEqual(filenames(self.collector.python_files()),
                         ['__init__.py', 'authorization.py'])

    def test_classes(self):
        classes = list(self.collector.classes())
        self.assertEqual(names(classes), ['Authorization', 'TrashClass'])

    def test_commands(self):
        commands = self.collector.commands()
        self.assertEqual(names(commands), ['Authorization'])

    def test_mapper(self):
        mapper = self.collector.mapper()
        self.assertEqual(mapper['user.authorization'].__name__,
                         'Authorization')