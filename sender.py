# coding: utf8

from common import Common
from packer import Packer
import pyamf
import socket


class Sender(Packer):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, data):
        data = self.encode(data)
        self.sock.send(self.pack(data))

    def recv(self, size=1024):
        return self.sock.recv(size)

    def parse(self):
        size = self.packsize(self.recv(self.SBIN_SIZE))
        data = self.unpack(size, self.recv(size))
        return self.decode(data)

    def close(self):
        self.sock.close()

