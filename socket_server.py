# coding: utf8

from listener import Listener
from ext.daemon import Daemon

class SocketServer(Daemon):

    def run(self):
        self.listener = Listener()
        self.listener.run()


if __name__ == '__main__':

    SocketServer('/tmp/socket_server2.pid').run()
