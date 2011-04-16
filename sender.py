# coding: utf8

from common import Common
from packer import Packer
import pyamf
import socket


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

class Sender(Common, Packer, BaseSender):

    def __init__(self, host, port):
        BaseSender.__init__(self, host, port)
#        BaseSender.send(self, '<policy-file-request/>\0')

    def send(self, data):
        data = pyamf.encode(data).read()
        return BaseSender.send(self, self.pack(data))
