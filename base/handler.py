# coding: utf8
from common import Common
from threading import Thread
import logging
import socket
import select


class BaseHandler(Common, Thread):

    port = 8885
    epoll_timeout = 2
    address = ''

    def __init__(self):
        Thread.__init__(self)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.address, self.port))
        self.socket.listen(5)
        self.socket.setblocking(0)

        self.epoll = select.epoll()
        self.epoll_register(self.socket)

    def epoll_register(self, socket, type=select.EPOLLIN):
        self.epoll.register(socket.fileno(), type)

    def register(self, sock, type=select.POLLIN):
        self.clients[sock.fileno()] = sock
        self.epoll_register(sock, type)

        logging.debug('register client %s' % len(self.clients))

    def modify(self, sock, type):
        self.epoll.modify(sock.fileno(), type)

    def unregister(self, filleno):
        self.epoll.unregister(filleno)
        sock = self.clients.get(filleno)
        if sock:
            sock.close()
            del self.clients[filleno]

    def get(self, no):
        return self.clients.get(no)

    def run(self):
        self.clients = {}
        self.buffer = {}

        while not self.epoll.closed:
            events = self.epoll.poll(self.epoll_timeout)
            for no, event in events:
                if no == self.socket.fileno():
                    sock, address = self.socket.accept()
                    self.register(sock)
                else:
                    self.process(self.get(no), event)


    def close(self):
        self.epoll.close()
        self.socket.close()

