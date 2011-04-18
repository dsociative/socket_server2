# coding: utf8

from handler import BaseHandler
from packer import Packer
import logging
import select
import socket

def log_debug(f):

    def wrapper(obj, *args, **kwargs):
        logging.debug('%s - %s' % (obj, f.func_name))

        return f(obj, *args, **kwargs)

    return wrapper

class Talker(BaseHandler, Packer):

    port = 8885

    def recv(self, sock, size):
        try:
            data = sock.recv(size)
            if not data:
                self.unregister(sock)
            else:
                return data
        except socket.error, s:
            logging.warning(s)
            self.unregister(sock)

    def process(self, sock, event):
        logging.debug('talker clients %s' % len(self.clients))

        if event & select.EPOLLIN:
            print 'IN'
            data = self.recv(sock, 1024)
            if data:
                size = self.packsize(data[:4])
                self.decode(self.unpack(size, data[4:]))
                self.modify(sock, select.EPOLLOUT)

        elif event & select.EPOLLOUT:
            print 'OUT'
            d = self.pack(self.encode({'command':'ok'}))
            sock.send(d + '\0')
            self.modify(sock, select.EPOLLIN)

