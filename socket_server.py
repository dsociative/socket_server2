# coding: utf8
from base.common import Common
from base.listener import PolicyCaster
from base.talker import Talker
from base.test.ze_mapper import Mapper
from ext.daemon import Daemon
from http.http_socket import HttpSocket
import logging
import os
import sys

class SocketServer(Daemon):

    def init_logging(self):
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        level = logging.DEBUG

        logging.basicConfig(format=format, level=level)

    def __init__(self, name, port, mapper, http_port=None):

        self.port = port
        self.mapper = mapper
        self.http_port = http_port


        def named(s):
            return s % name

        def named_path(s):
            return os.path.abspath(named(s))


        Daemon.__init__(self, named('/tmp/socket_%s.pid'),
                        stderr=named_path('error_%s.log'),
                        stdout=named_path('out_%s.log'))

    def run(self):
        self.init_logging()
        Talker.port = self.port
        Common.mapper = self.mapper


        self.talker = Talker()
#        self.polisy_caster = PolicyCaster()
#        self.polisy_caster.start()
        if self.http_port:
            self.http_socket = HttpSocket(self.mapper, self.http_port)
        self.talker.run()

    def close(self, *q):
#        self.polisy_caster.close()
        if self.http_port:
            self.http_socket.stop()
        self.talker.close()
        sys.exit(0)


if __name__ == '__main__':
    server = SocketServer('test', 8885, Mapper())
    if 'start' in sys.argv:
        server.start()
    elif 'stop' in sys.argv:
        server.stop()
    else:
        server.run()
