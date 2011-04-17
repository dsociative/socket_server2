# coding: utf8

from common import Common
from talker import Talker
from threading import Thread
import logging
import socket
import time

class Listener(Common, Thread):

    status = False
    port = 8885

    def __init__(self):
        Thread.__init__(self)
        self.queue_size = 32
        self.bind()
        self.clients = []

    def bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', self.port))
        sock.listen(self.queue_size)
        self.srv = sock


    def run(self):
        Listener.status = True
        while Listener.status:
            self.read()

    def read(self):
        sock, addr = self.srv.accept()

        talker = Talker(sock)
        talker.start()

        self.clients.append(talker)

    def close(self):
        try:
            self.srv.shutdown(socket.SHUT_RDWR)
        except socket.error, err:
            logging.warning(err)
        self.srv.close()
        Listener.status = False

class PolicyListener(Listener):

    port = 843

    def read(self):
        self.srv.listen(self.queue_size)
        socket, addr = self.srv.accept()

        socket.send(self.policy_xml)
        socket.close()

