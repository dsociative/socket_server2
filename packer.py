# coding: utf8

import _struct as struct
import pyamf

class Packer():

    SBIN_SIZE = 4

    def pack(self, data):
        size = len(data)
        print size
        data = struct.pack('!I%ss' % size, size, data)
        return data

    def packsize(self, sbinary):
        if sbinary and len(sbinary) == self.SBIN_SIZE:
            return struct.unpack('!I', sbinary)[0]

    def unpack(self, size, data):
        if size:
            return data[:size]

    def decode(self, data):
        data = pyamf.decode(data).readElement()
        if data:
            return data

    def encode(self, params):
        data = pyamf.encode(params)
        return data.read()
