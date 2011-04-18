# coding: utf8

from ext.daemon import Daemon
from listener import PolicyCaster
from talker import Talker
from test.test_case import *
import signal
import sys
import socket, select

class SocketServer(Daemon):

    def __init__(self):
        Daemon.__init__(self, '/tmp/socket_server2.pid')

    def run(self):
        self.talker = Talker()
        self.polisy_caster = PolicyCaster()
        self.polisy_caster.start()
        self.talker.run()
        self.close()

    def close(self, *q):
        self.polisy_caster.working = False
        self.talker.working = False
        self.polisy_caster.close()
        self.talker.close()
        sys.exit(0)




if __name__ == '__main__':
    server = SocketServer()
    signal.signal(signal.SIGINT, server.close)
    server.run()
