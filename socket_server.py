# coding: utf8

from common import Common
from ext.daemon import Daemon
from listener import PolicyCaster
from talker import Talker
from test.test_case import *
from test.ze_mapper import Mapper
import os
import sys

class SocketServer(Daemon):

    def __init__(self, name, port, mapper):

        self.port = port
        self.mapper = mapper

        def named(s):
            return s % name

        def named_path(s):
            return os.path.abspath(named(s))


        Daemon.__init__(self, named('/tmp/socket_%s.pid'),
                        stderr=named_path('error_%s.log'),
                        stdout=named_path('out_%s.log'))

    def run(self):
        Talker.port = self.port
        Common.mapper = self.mapper


        self.talker = Talker()
        self.polisy_caster = PolicyCaster()
        self.polisy_caster.start()
        self.talker.run()

    def close(self, *q):
        self.polisy_caster.close()
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
