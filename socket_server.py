# coding: utf8

from ext.daemon import Daemon
from listener import Listener, PolicyListener
import logging

class SocketServer(Daemon):

    def run(self):
        logging_frm = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging_level = logging.DEBUG
        logging.basicConfig(format=logging_frm, level=logging_level)


        self.listener = Listener()
        self.policy_listener = PolicyListener()
        self.policy_listener.start()
        self.listener.run()


if __name__ == '__main__':

    SocketServer('/tmp/socket_server2.pid').run()
