# coding:utf8

from socket_server.base.talker import Talker
from socket_server.client.test_client import TestClient
from test import TestCase
import socket
import time


class FakeSocket(object):

    def fileno(self):
        return 0


def wait_for(func, tick=0.01, out=1):
    i = 0.0
    while i < out and not func():
        print i
        time.sleep(tick)
        i += tick


class ClientsMapTest(TestCase):

    def setUp(self):
        self.talker = Talker(client_cls=TestClient)
        self.map = self.talker.clients

        self.talker.start()
        self.sock = socket.socket()

    def tearDown(self):
        self.sock.close()
        self.talker.stop()

    def test_socket_client_init(self):
        self.assertEqual(self.map.clients, {})

        self.sock.connect(('localhost', self.talker.port))
        wait_for(lambda: self.map.clients)

        self.assertEqual(len(self.map.clients), 1)
        client = self.map.clients.values()[0]
        self.assertIsInstance(client, TestClient)

        self.sock.close()
        wait_for(lambda: not self.map.clients)
        self.assertEqual(self.map.clients, {})
