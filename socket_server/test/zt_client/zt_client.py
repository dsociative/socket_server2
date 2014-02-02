# coding: utf8

from socket_server.base.talker import Talker
from socket_server.client.test_client import TestClient
from socket_server.test import TestCase
from socket_server.util.sender import Sender
import time


AUTH_DICT = {"command": "user.authorization", "uid": "6104128459101111038",
             "auth_key": "599bf8e08afc3003d0db1a7f048eee49"}


class Zt_Base(TestCase):
    def wait(self):
        time.sleep(self.talker.epoll_timeout * 2)

    def create_sender(self):
        return Sender('', self.talker.port)

    def setUp(self):
        TestClient.disconnected = []
        self.talker = Talker(port=64533, client_cls=TestClient)
        Talker.port = 64536

        self.talker.start()
        self.wait_equal(self.talker.is_alive, True)
        self.sender = self.create_sender()
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
        self.wait()
        self.client = self.first_client()

    def first_client(self):
        return self.talker.clients.by_fileno.values()[0]

    def wait_disconnect(self, client):
        self.wait_equal(lambda: TestClient.disconnected, [client.id])

    def test_reply(self):
        request = {'hello': 'world'}

        self.client.add_resp(request)
        sender_response = self.sender.parse()
        self.assertEqual(sender_response, request)

    def test_hung_up(self):
        client = self.first_client()
        client.hung_up()
        self.wait_disconnect(client)
        self.wait_equal(lambda: self.talker.clients.by_fileno.values(), [])

    def test_hung_up_disconned(self):
        client = self.first_client()
        self.sender.socket.close()
        time.sleep(2)
        client.hung_up()
        self.wait_disconnect(client)
        self.wait_equal(lambda: self.talker.clients.by_fileno.values(), [])

    def test_disconnect_on_error(self):
        client = self.first_client()
        data = self.sender.encode({'1': '3'}).replace('}', '^')
        self.sender.socket.send(data)
        self.wait_disconnect(client)
        self.wait_equal(lambda: self.talker.clients.by_fileno.values(), [])

    def test_hung_up_closed(self):
        client = self.first_client()
        client.sock.close()
        self.wait_disconnect(client)

    def test_disconnect_event(self):
        TestClient.disconnected = []
        client = self.first_client()
        self.sender.close()
        self.wait_disconnect(client)
