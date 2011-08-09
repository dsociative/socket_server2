# coding: utf8
from base.common import Common
from base.talker import Talker
from base.test.ze_mapper import Mapper
from ext.daemon import Daemon
from http.http_socket import HttpSocket
import logging
import os
import sys

from signal import signal, SIGTERM, SIGINT

class SocketServer(Daemon):

    def init_logging(self):
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        level = logging.DEBUG

        logging.basicConfig(format=format, level=level)

    def __init__(self, name, config, mapper):

        self.mapper = mapper
        self.http_port = config.getint('sockets', 'http_port')

        Talker.port = config.getint('sockets', 'socket_port')
        self.talker = Talker(config)

        def named(s):
            return s % name

        def named_path(s):
            return os.path.abspath(named(s))


        Daemon.__init__(self, named('/tmp/socket_%s.pid'),
                        stderr=named_path('error_%s.log'),
                        stdout=named_path('out_%s.log'))

    def run(self):
        self.init_logging()
        Common.mapper = self.mapper

        for sig in (SIGTERM, SIGINT):
            signal(sig, lambda signum, stack_frame: self.close(1))

        if self.http_port:
            self.http_socket = HttpSocket(self.mapper, self.http_port)
        self.talker.run()

    def close(self, *q):
        if self.http_port:
            self.http_socket.stop()
        self.talker.close()
        print 'is closed'
        sys.exit(0)


if __name__ == '__main__':
    daemon = SocketServer('test', 8885, Mapper())
    if daemon.process_argv():
        pass
    else:
        daemon.run()

