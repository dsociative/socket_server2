# coding: utf8

from socket import socket

from socket_server.base.talker import Talker
from socket_server.client.base_client import BaseClient
from socket_server.test import TestCase


class BaseClientTest(TestCase):

    def setUp(self):
        self.talker = Talker()

    def test_init_id(self):
        no = BaseClient.count
        client = BaseClient(socket(), None, self.talker)
        self.assertEqual(client.id, no + 1)
        client = BaseClient(socket(), None, self.talker)
        self.assertEqual(client.id, no + 2)
