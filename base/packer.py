# coding: utf8

import _struct as struct
import pyamf

class PackerDecodeError(Exception):
    pass

class Packer():

    SBIN_SIZE = 4

    def pack(self, data):
        size = len(data)
        data = struct.pack('!I%ss' % size, size, data)
        return data

    def packsize(self, sbinary):
        if sbinary and len(sbinary) == self.SBIN_SIZE:
            return struct.unpack('!I', sbinary)[0]
        else:
            raise PackerDecodeError('Error size')

    def unpack(self, size, data):

        if not size:
            raise PackerDecodeError('size not found')
        elif size != len(data):
            raise PackerDecodeError('size:%s != data length:%s' % (size, len(data)))

        return pyamf.decode(data).readElement()

    def split(self, data):
        return data[:self.SBIN_SIZE], data[self.SBIN_SIZE:]

    def decode(self, data):
        if len(data) <= 4:
            raise PackerDecodeError('lenght <= 4')

        sbin, data = self.split(data)
        return self.unpack(self.packsize(sbin), data)

    def encode(self, params):
        data = pyamf.encode(params)
        return self.pack(data.read()) + '\0'
