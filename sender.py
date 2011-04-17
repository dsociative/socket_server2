# coding: utf8

from packer import Packer
import logging
import socket


class Sender(Packer):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))
        return self

    def send(self, data):
        data = self.encode(data)
        self.socket.send(self.pack(data))

    def recv(self, size=1024):
        return self.socket.recv(size)

    def parse(self):
        size = self.packsize(self.recv(self.SBIN_SIZE)) + 1
        data = self.unpack(size, self.recv(size))
        return self.decode(data)

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error, err:
            logging.warning(err)
        self.socket.close()
        self.status = False

