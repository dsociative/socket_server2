# coding: utf8

from common import Common
from talker import Talker
from threading import Thread
import socket

class Listener(Common, Thread):

    status = True
    port = 8885

    def __init__(self):
        Thread.__init__(self)
        self.queue_size = 32
        self.bind()
        self.sockets = []

    def bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', self.port))
        self.srv = sock


    def run(self):
        self.policy_listener = PolicyListener()
        self.policy_listener.start()
        while self.srv and self.status:
            self.read()

    def read(self):
        self.srv.listen(self.queue_size)
        sock, addr = self.srv.accept()
        print 'new connection'
        Talker(sock).start()


    def close(self):
        self.status = False
        if self.srv:
            self.srv.close()
            self.srv = None

class PolicyListener(Listener):

    port = 843

    def read(self):
        self.srv.listen(self.queue_size)
        socket, addr = self.srv.accept()

        socket.send(self.policy_xml)
        socket.close()

