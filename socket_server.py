# coding: utf8

from ext.daemon import Daemon
from listener import Listener, PolicyListener
from test.test_case import *

class SocketServer(Daemon):

    def run(self):
        self.listener = Listener()
        self.policy_listener = PolicyListener()
        self.policy_listener.start()
        self.listener.run()


if __name__ == '__main__':

    SocketServer('/tmp/socket_server2.pid').run()
