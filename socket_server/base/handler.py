# coding: utf8

from redis.client import Redis
from socket_server.base.clients_map import ClientsMap
from socket_server.base.common import Common, trace
from socket_server.client.simple_client import SimpleClient
from threading import Thread
import logging
import select
import socket


class BaseHandler(Common, Thread):

    epoll_timeout = 2

    def __init__(self, port=8885, address='', redis=Redis(),
                 client_cls=SimpleClient):
        Thread.__init__(self)
        self.client_cls = client_cls
        self.port = port
        self.socket = self.create_socket(port, address)
        self.fileno = self.socket.fileno()

        self.epoll = select.epoll()
        self.epoll_register(self.socket)

        self.clients = ClientsMap(self)

    def create_socket(self, port, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((address, port))
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
        try:
            self.epoll.modify(sock.fileno(), type)
        except:
            trace()

    def unregister(self, filleno):
        sock = self.clients.get(filleno)
        if sock:
            try:
                self.epoll.unregister(filleno)
                sock.close()
            except:
                trace()
            del self.clients[filleno]

    def accept(self):
        sock, address = self.socket.accept()
        sock.setblocking(0)
        return self.register(sock, address)

    def run(self):
        self.request = {}

        while not self.epoll.closed:
            events = self.epoll.poll(self.epoll_timeout)
            for no, event in events:
                if no == self.fileno:
                    self.accept()
                else:
                    client = self.clients.get(no)
                    if client:
                        self.process(client, event)

    def stop(self):
        self.unregister(self.fileno)
        self.epoll.close()
        self.socket.close()

