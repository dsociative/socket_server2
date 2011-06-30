# coding:utf8
from base.client import Client
from base.clients_map import ClientsMap
from base.test.test_case import TestCase


class ClientsMapTest(TestCase):

    def setUp(self):
        self.map = ClientsMap()


    def test_client(self):
        client = Client(None, None, None)
        self.map[1] = client
        self.assertEqual(self.map[1], client)

        client.uid = '200'
        self.map.add_user(client)
        self.assertEqual(self.map.users['200'], self.map[1])

        del self.map[1]
        self.assertEqual(self.map[1], None)
        self.assertEqual(self.map.users.get('200'), self.map[1])
