# coding: utf8

from socket_server.base.packer import Packer
from socket_server.test import TestCase
import json


class Zt_Packer(TestCase):

    def setUp(self):
        self.data = {'param1': 'param2', '1': 123, 'q': {'other': 'me'}}
        self.packer = Packer()

    def test_data(self):
        self.encoded = self.packer.encode(self.data)
        self.assertEqual(self.packer.decode(self.encoded), self.data)

    def test_pack_size(self):
        size = len(json.dumps(self.data))
        sbin = self.packer.encode(self.data)[:self.packer.SBIN_SIZE]
        self.assertEqual(self.packer.packsize(sbin), size)

