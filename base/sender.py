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
        self.socket.send(self.encode(data))

    def recv(self):
        size_data = None
        while not size_data:
            size_data = self.socket.recv(4)

        size = self.packsize(size_data)

        return size, self.socket.recv(size)

    def parse(self):
        return self.decode(*self.recv())

    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error, err:
            logging.warning(err)
        self.socket.close()
        self.status = False

