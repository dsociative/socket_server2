# coding:utf8

from base.client import Client
from base.talker import Talker
from test import TestCase
from test.ze_commands.ze_mapper import Mapper
import socket
import time


class TestClient(Client):

    def __init__(self, sock, talker, uid=None):
        Client.__init__(self, sock, None, talker, uid=uid)
        self.resp = None

    def add_resp(self, resp):
        self.resp = resp


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
        self.talker = Talker(Mapper())
        self.map = self.talker.clients

        self.talker.start()
        self.sock = socket.socket()

    def tearDown(self):
        self.sock.close()
        self.talker.stop()
        self.map.subcriber.stop()

    def test_socket_client_init(self):
        self.assertEqual(self.map.clients, {})

        self.sock.connect(('localhost', self.talker.port))
        wait_for(lambda: self.map.clients)

        self.assertEqual(len(self.map.clients), 1)
        client = self.map.clients.values()[0]
        self.assertIsInstance(client, Client)

        self.sock.close()
        wait_for(lambda: not self.map.clients)
        self.assertEqual(self.map.clients, {})

    def test_client(self):
        client = Client(FakeSocket(), None, self.talker)
        self.map[1] = client
        self.assertEqual(self.map[1], client)

        self.map.add_user(client, '200')
        self.assertEqual(self.map.users['200'], self.map[1])

        del self.map[1]
        self.assertEqual(self.map[1], None)
        self.assertEqual(self.map.users.get('200'), None)

    def test_client_response(self):
        client = TestClient(FakeSocket(), self.talker)
        self.map.add_user(client, '1500uid')
        test_msg = {'msg': 1}
        self.map.queue((client.uid,), test_msg)
        self.assertEqual(client.resp, test_msg)

    def test_client_send(self):
        import time
        client = TestClient(FakeSocket(), self.talker)
        time.sleep(1)
        self.map.add_user(client, '1500uid')
        test_msg = {'msg': 1}
        self.map.send(test_msg, '1500uid')
        del test_msg['uids']
        time.sleep(1)
        self.assertEqual(client.resp, test_msg)
