# coding: utf8

from ext.daemon import Daemon
from listener import Listener, PolicyListener
from test.test_case import *
import signal


class SocketServer(Daemon):

    def run(self):
        self.listener = Listener()
        self.policy_listener = PolicyListener()
        self.policy_listener.start()
        self.listener.run()

    def close(self, *q):
        self.listener.close()
        self.policy_listener.close()




if __name__ == '__main__':
    server = SocketServer('/tmp/socket_server2.pid')
    signal.signal(signal.SIGINT, server.close)
    server.run()
