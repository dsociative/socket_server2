# coding: utf8

from test.test_case import TestCase
import pyamf

class Zt_Packer(TestCase):

    def setUp(self):
        self.data = {'param1':'param2', 'q':{'other':'me'}}
        self.binary = pyamf.encode(self.data).read()
        self.packer = Packer()

    def test_(self):
        packed = self.packer.pack(self.binary)
        size = self.packer.packsize(packed[:self.packer.SBIN_SIZE])
        self.assertEqual(self.packer.unpack(size, packed[self.packer.SBIN_SIZE:]),
                         self.binary)

