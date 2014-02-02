# coding:utf8
import socket
import time

from socket_server.base.talker import Talker
from socket_server.client.test_client import TestClient
from socket_server.test import TestCase


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
        self.assertEqual(self.map.by_fileno, {})

        self.sock.connect(('localhost', self.talker.port))
        wait_for(lambda: self.map.by_fileno)

        self.assertEqual(len(self.map.by_fileno), 1)
        client = self.map.by_fileno.values()[0]
        self.assertIsInstance(client, TestClient)
        self.assertEqual(client, self.map.by_cid[client.id])

        self.sock.close()
        wait_for(lambda: not self.map.by_fileno)
        self.assertEqual(self.map.by_fileno, {})

    def test_queue(self):
        client = TestClient(FakeSocket(), None, self.talker)
        self.map[0] = client
        self.map.queue([client.id], 'hello')
        self.assertEqual(client.queue, ['hello'])
