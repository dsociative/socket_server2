# coding: utf8
from base.common import Common, init_logging
from base.talker import Talker
from http.http_socket import HttpSocket
from threading import Thread
import os
import sys



class SocketServer(Thread):

    def __init__(self, name, config, mapper, urls={}):
        Thread.__init__(self)

        self.mapper = mapper
        self.http_port = config.getint('sockets', 'http_port')

        Talker.port = config.getint('sockets', 'socket_port')
        self.talker = Talker(config)

        def named(s):
            return s % name

        def named_path(s):
            return os.path.abspath(named(s))

        init_logging()
        Common.mapper = self.mapper

        if self.http_port:
            self.http_socket = HttpSocket(self.mapper, self.http_port, ulrs=urls)
            self.http_socket.start()


    def run(self):
        self.talker.run()

    def stop(self, *q):
        if self.http_port:
            self.http_socket.stop()
        self.talker.stop()
        print 'socket is closed'
        sys.exit(0)

