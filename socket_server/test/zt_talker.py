# coding: utf8

from socket_server.base.talker import Talker
from socket_server.client.test_client import TestClient
from socket_server.util.sender import Sender
from test import TestCase
import random
import time


class Zt_Talker_Base(TestCase):

    def setUp(self):
        port = random.choice(range(5000, 6500))
        Talker.epoll_timeout = 0.1
        self.talker = Talker(port=port, client_cls=TestClient)
        self.talker.start()
        self.sender = Sender('', port)

    def tearDown(self):
        self.talker.stop()
        time.sleep(Talker.epoll_timeout)


class Zt_Talker_Threading(Zt_Talker_Base):

    def test_init(self):
        self.wait_equal(self.talker.is_alive, True)

    def test_close(self):
        self.wait_equal(self.talker.is_alive, True)
        self.talker.stop()
        self.wait_equal(self.talker.is_alive, False)


class Zt_Talker(Zt_Talker_Base):

    def setUp(self):
        Zt_Talker_Base.setUp(self)
        self.sender.connect()
        self.data = {"command": "user.authorization",
                     "uid": "6104128459101111038",
                     "auth_key": "599bf8e08afc3003d0db1a7f048eee49"}

    def test_command(self):
        self.sender.send(self.data)
        self.assertEqual(self.sender.parse(), 'hello')
