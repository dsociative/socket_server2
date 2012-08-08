# coding: utf8

from base.talker import Talker
from threading import Thread
import os
import sys


class SocketServer(Thread):

    def __init__(self, name, config, mapper, auth_func, urls={}):
        Thread.__init__(self)

        self.mapper = mapper
        self.talker = Talker(mapper,
                             port=config.getint('sockets', 'socket_port'),
                             db_channel=config.get('sockets', 'db_channel'))

        def named(s):
            return s % name

        def named_path(s):
            return os.path.abspath(named(s))

    def run(self):
        self.talker.run()

    def stop(self, *q):
        if self.http_port:
            self.http_socket.stop()
        self.talker.stop()
        print 'socket is closed'
        sys.exit(0)
