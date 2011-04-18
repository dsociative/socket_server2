# coding: utf8

from sender import Sender
from socket_server import SocketServer
from talker import Talker
from test.test_case import TestCase
import thread
import time

class Zt_Talker_Base(TestCase):

    def tearDown(self):
        pass
#        self.talker.close()


class Zt_Talker_Threading(Zt_Talker_Base):

    def setUp(self):
        self.talker = Talker()
        self.talker.start()
        time.sleep(0.4)
        self.sender = Sender('', self.talker.port)

    def test_init(self):
        self.wait_equal(self.talker.is_alive, True)

    def test_close(self):
        self.wait_equal(self.talker.is_alive, True)
        self.talker.close()
        time.sleep(0.4)
        self.wait_equal(self.talker.is_alive, False)

    def test_client_out(self):
        self.sender.connect()
        time.sleep(0.2)

        talker = self.listener.clients[0]
        self.assertTrue(isinstance(talker, Talker))
        self.wait_equal(talker.is_alive, True)
        self.sender.close()
        self.wait_equal(talker.is_alive, False)


class Zt_Talker(Zt_Talker_Base):

    def setUp(self):
        self.talker = Talker()
        self.talker.start()
        time.sleep(1)
        self.sender = Sender('', 8885).connect()
        self.data = {"command": "user.authorization",
                     "uid": "6104128459101111038",
                     "auth_key": "599bf8e08afc3003d0db1a7f048eee49"}

    def test_command(self):
        self.sender.send(self.data)
        self.assertEqual(self.sender.parse()['result'], 1)

