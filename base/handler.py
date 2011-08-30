# coding: utf8

from base.clients_map import ClientsMap
from base.common import trace
from common import Common
from threading import Thread
import logging
import select
import socket


class BaseHandler(Common, Thread):

    port = 8885
    epoll_timeout = 2
    address = ''


    def __init__(self, config):
        Thread.__init__(self)

        self.socket = self.create_socket()
        self.fileno = self.socket.fileno()

        self.epoll = select.epoll()
        self.epoll_register(self.socket)

        self.clients = ClientsMap(self, config)

    def create_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.address, self.port))
        sock.listen(2)
        sock.setblocking(0)
        return sock

    def epoll_register(self, socket, type=select.EPOLLIN):
        self.epoll.register(socket.fileno(), type)

    def register(self, sock, address, type=select.POLLIN):
        self.clients[sock.fileno()] = sock
        self.epoll_register(sock, type)

        logging.debug('register client %s' % len(self.clients))

    def modify(self, sock, type):
        self.epoll.modify(sock.fileno(), type)

    def unregister(self, filleno):
        self.epoll.unregister(filleno)
        sock = self.clients.get(filleno)
        if sock:
            try:
                sock.close()
            except:
                trace()
            del self.clients[filleno]

    def get(self, no):
        return self.clients.get(no)


    def accept(self):
        sock, address = self.socket.accept()
        return self.register(sock, address)

    def run(self):
        self.buffer = {}

        while not self.epoll.closed:
            events = self.epoll.poll(self.epoll_timeout)
            for no, event in events:
                if no == self.fileno:
                    self.accept()
                else:
                    self.process(self.get(no), event)


    def stop(self):
        self.epoll.close()
        self.socket.close()

