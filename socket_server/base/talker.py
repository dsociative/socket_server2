# coding: utf8
from handler import BaseHandler
from packer import Packer
import select


class Talker(BaseHandler, Packer):

    def register(self, sock, addr, etype=select.POLLIN):
        self.clients[sock.fileno()] = self.client_cls(sock, addr, self)
        self.epoll_register(sock, etype)

    def process(self, client, event):
        if event & select.EPOLLIN:
            client.recv()
        elif event & select.EPOLLOUT:
            client.reply()
        elif event & select.EPOLLHUP or event & select.EPOLLERR:
            self.unregister(client.fileno)
