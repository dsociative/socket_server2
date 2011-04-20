# coding: utf8

from sender import Sender
from talker import Talker
from test.test_case import TestCase
import time

class Zt_Base(TestCase):

    def setUp(self):
        Talker.epoll_timeout = 0.1
        self.talker = Talker()
        self.talker.start()
        self.wait_equal(self.talker.is_alive, True)
        self.sender = Sender('', self.talker.port)

    def tearDown(self):
        self.talker.close()
        time.sleep(Talker.epoll_timeout)


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

    def test_reply(self):
        response = {'hello':'world'}

        self.sender.connect()
        time.sleep(Talker.epoll_timeout)
        client = self.talker.clients.values().pop()
        client.add_resp(response)
        sender_request = self.sender.parse()
        self.assertEqual(sender_request, response)

    def test_login(self):

        data = {"command": "user.authorization",
                 "uid": "6104128459101111038",
                 "auth_key": "599bf8e08afc3003d0db1a7f048eee49"}

        self.sender.connect()
        time.sleep(Talker.epoll_timeout)
        client = self.talker.clients.values().pop()

        self.assertEqual(client.logged, False)
        self.sender.send(data)
        time.sleep(Talker.epoll_timeout)
        self.assertEqual(client.logged, True)



