# coding: utf8

from talker import Talker
from threading import Thread
import socket

class Listener(Thread):

    status = True

    def __init__(self):
        Thread.__init__(self)
        self.port = 8885
        self.queue_size = 32
        self.bind()
        self.sockets = []

    def bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        self.srv = sock

    def run(self):
        while self.srv and self.status:
            self.read()

    def read(self):
        self.srv.listen(self.queue_size)
        sock, addr = self.srv.accept()
#        pal = sock.recv(1024)
        Talker(sock).start()

    def close(self):
        self.status = False
        if self.srv:
            self.srv.close()
            self.srv = None
