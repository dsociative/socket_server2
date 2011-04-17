# coding: utf8

from handler import BaseHandler
from packer import Packer
import logging
import select

def log_debug(f):

    def wrapper(obj, *args, **kwargs):
        logging.debug('%s - %s' % (obj, f.func_name))

        return f(obj, *args, **kwargs)

    return wrapper

class Talker(BaseHandler, Packer):

    port = 8885

    def process(self, sock, event):
        if event & select.EPOLLIN:
            if sock.fileno() in self.buffer:
                data = sock.recv(1024)
                self.modify(sock, select.EPOLLOUT)
#                data = sock.recv(1024)
#                size = self.packsize(data[:4])
#                print size
#                if size:
#                    print self.decode(self.unpack(size, data[size:]))
#                del self.buffer[sock.fileno()]
#                self.modify(sock, select.EPOLLOUT)
#            else:
#                self.buffer[sock.fileno()] = sock.recv(self.SBIN_SIZE)
#                self.modify(sock, select.EPOLLIN)
        elif event & select.EPOLLOUT:
            print "OUT!!!!!!!!!"
            d = self.pack({'qwe':1})
            sock.send(self.encode(d) + '\0')
            self.modify(sock, select.EPOLLIN)
#            self.unregister(sock)
