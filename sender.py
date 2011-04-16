# coding: utf8

from packer import Packer
import socket
import pyamf


class BaseSender(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, data):
        self.sock.send(data)
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()

class Sender(BaseSender):

    packer = Packer()

    def send(self, data):
        data = pyamf.encode(data).read()
        return BaseSender.send(self, self.packer.pack(data))
