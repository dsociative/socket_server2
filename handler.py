# coding: utf8
from common import Common
from threading import Thread
import logging
import socket
import select


class BaseHandler(Common, Thread):

    working = True
    port = 8885
    address = ''

    def __init__(self):
        Thread.__init__(self)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.address, self.port))
        self.socket.listen(200)
        self.socket.setblocking(0)

    def epoll_register(self, socket, type=select.EPOLLIN):
        self.epoll.register(socket.fileno(), type)

    def register(self, sock, type=select.POLLIN):
        self.clients[sock.fileno()] = sock
        self.epoll_register(sock, type)

        logging.debug('register client %s' % len(self.clients))

    def modify(self, sock, type):
        self.epoll.modify(sock.fileno(), type)

    def unregister(self, sock):
        self.epoll.unregister(sock.fileno())
#        sock.shutdown(socket.SHUT_WR)
        del self.clients[sock.fileno()]
        if self.buffer.has_key(sock.fileno()):
            del self.buffer[sock.fileno()]
        sock.close()

    def get(self, no):
        return self.clients.get(no)

    def run(self):
        self.epoll = select.epoll()
        self.epoll_register(self.socket)
        self.clients = {}
        self.buffer = {}

        while self.working:
            events = self.epoll.poll(200)
            for no, event in events:
                if no == self.socket.fileno():
                    sock, address = self.socket.accept()
                    self.register(sock)
                else:
                    self.process(self.get(no), event)

    def close(self):
        self.epoll.unregister(self.socket.fileno())
        self.epoll.close()
        self.socket.close()

