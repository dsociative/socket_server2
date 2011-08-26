# coding: utf8
from base.common import Common
from base.talker import Talker
from http.http_socket import HttpSocket
import logging
import os
import sys

from threading import Thread


class SocketServer(Thread):

    def init_logging(self):
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        level = logging.DEBUG

        logging.basicConfig(format=format, level=level)

    def __init__(self, name, config, mapper):
        Thread.__init__(self)

        self.mapper = mapper
        self.http_port = config.getint('sockets', 'http_port')

        Talker.port = config.getint('sockets', 'socket_port')
        self.talker = Talker(config)

        def named(s):
            return s % name

        def named_path(s):
            return os.path.abspath(named(s))
        self.init_logging()
        Common.mapper = self.mapper

        if self.http_port:
            self.http_socket = HttpSocket(self.mapper, self.http_port)


    def run(self):
        self.talker.run()

    def close(self, *q):
        if self.http_port:
            self.http_socket.stop()
        self.talker.close()
        print 'socket is closed'

