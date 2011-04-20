# coding: utf8

from client import Client
from common import Common
from handler import BaseHandler
from packer import Packer
import logging
import select
import socket

class Talker(BaseHandler, Packer):

    port = 8885

    def register(self, sock, type=select.POLLIN):
        self.clients[sock.fileno()] = Client(sock, self.epoll)
        self.epoll_register(sock, type)
        logging.debug('register client %s' % len(self.clients))

    def recv(self, sock, size):
        try:
            data = sock.recv(size)
            if not data:
                self.unregister(sock.fileno())
            else:
                return data
        except socket.error, s:
            logging.warning(s)
            self.unregister(sock.fileno())

    def process(self, client, event):
        logging.debug('talker clients %s' % len(self.clients))

        if event & select.EPOLLIN:
            data = self.recv(client.sock, 1024)
            if data:
                client.listen(self.decode(data))

        elif event & select.EPOLLOUT:
            if client.has_reponse:
                client.reply()

