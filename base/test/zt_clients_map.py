# coding:utf8
from base.client import Client
from base.clients_map import ClientsMap
from base.test.test_case import TestCase

class TestClient(Client):

    def __init__(self, sock, uid=None):
        Client.__init__(self, sock, None, None, uid=uid)
        self.resp = None

    def add_resp(self, resp):
        self.resp = resp

class FakeSocket(object):

    def fileno(self):
        return 0


class ClientsMapTest(TestCase):

    def setUp(self):
        self.map = ClientsMap(None)


    def tearDown(self):
        self.map.subcriber.stop()

    def test_client(self):
        client = Client(FakeSocket(), None, None)
        self.map[1] = client
        self.assertEqual(self.map[1], client)

        self.map.add_user(client, '200')
        self.assertEqual(self.map.users['200'], self.map[1])

        del self.map[1]
        self.assertEqual(self.map[1], None)
        self.assertEqual(self.map.users.get('200'), self.map[1])

    def test_client_response(self):
        client = TestClient(FakeSocket())
        self.map.add_user(client, '1500uid')
        test_msg = {'msg':1}
        self.map.response((client.uid,), test_msg)
        self.assertEqual(client.resp, test_msg)


    def test_client_send(self):
        import time
        client = TestClient(FakeSocket())
        time.sleep(1)
        self.map.add_user(client, '1500uid')
        test_msg = {'msg':1}
        self.map.send(test_msg, '1500uid')
        time.sleep(1)
        self.assertEqual(client.resp, test_msg)
