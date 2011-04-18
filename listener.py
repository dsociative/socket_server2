# coding: utf8

from handler import BaseHandler
import select


class PolicyCaster(BaseHandler):

    port = 843

    def process(self, sock, event):

        if event is select.POLLIN:
            self.modify(sock, select.EPOLLOUT)
        elif event is select.EPOLLOUT:
            sock.send(self.policy_xml + '\0')
            self.unregister(sock)
