# coding: utf8

from base.talker import Talker
from test import TestCase
from test.ze_commands.ze_mapper import Mapper
from util.sender import Sender
import time


class Zt_Base(TestCase):

    def wait(self):
        time.sleep(Talker.epoll_timeout * 2)

    def setUp(self):
        self.wait()
        self.talker = Talker(Mapper(), port=64533)
        Talker.epoll_timeout = 0.1
        Talker.port = 64536

        self.talker.start()
        self.wait_equal(self.talker.is_alive, True)
        self.sender = Sender('', self.talker.port)
        self.wait()

    def tearDown(self):
        self.talker.stop()
        self.wait()


class Zt_Client_Connection(Zt_Base):

    def test_client_on_connect(self):
        self.assertEqual(len(self.talker.clients), 0)
        self.sender.connect()
        time.sleep(Talker.epoll_timeout)
        self.assertEqual(len(self.talker.clients), 1)

    def test_client_on_disconnect(self):
        self.sender.connect()
        time.sleep(Talker.epoll_timeout)
        self.assertEqual(len(self.talker.clients), 1)
        self.sender.close()
        time.sleep(Talker.epoll_timeout)
        self.assertEqual(len(self.talker.clients), 0)


class Zt_Clien_Socket(Zt_Base):

    def setUp(self):
        Zt_Base.setUp(self)
        self.sender.connect()
        time.sleep(Talker.epoll_timeout)
        self.client = self.pop_client()

    def pop_client(self):
        return self.talker.clients.clients.values().pop()

    def test_reply(self):
        request = {'hello': 'world'}

        self.client.add_resp(request)
        sender_response = self.sender.parse()
        self.assertEqual(sender_response, request)

    def test_login(self):

        data = {"command": "user.authorization",
                 "uid": "6104128459101111038",
                 "auth_key": "599bf8e08afc3003d0db1a7f048eee49"}

        self.client = self.pop_client()

        self.assertEqual(self.client.logged, False)
        self.sender.send(data)
        time.sleep(Talker.epoll_timeout)
        self.assertEqual(self.client.logged, True)

