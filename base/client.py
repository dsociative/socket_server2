# coding:
from common import Common
from packer import Packer
import select
import logging

class Client(Common, Packer):

    def __init__(self, sock, poll, uid=None):
        self.sock = sock
        self.poll = poll
        self.uid = uid

        self.response = []
        self.peername = self.sock.getpeername()

    @property
    def logger(self):
        return logging.getLogger('Client %s - %s' % (self.peername, self.uid))

    def listen(self, params):
        name = params.get('command')
        cmd = self.mapper.get(name, self.uid)
        self.logger.info('command %s recieved' % name)
        if cmd:
            self.add_resp(cmd(self)(params))
        else:
            self.logger.warning('%s command not found' % name)

    def add_resp(self, resp):
        self.response.insert(0, resp)
        self.refresh_state()

    def reply(self):
        resp = self.response.pop()
        self.sock.send(self.encode(resp))
        self.refresh_state()

    @property
    def fileno(self):
        return self.sock.fileno()

    def close(self):
        return self.sock.close()

    @property
    def has_reponse(self):
        return len(self.response) > 0

    def refresh_state(self):
        type = select.EPOLLOUT if self.has_reponse else select.EPOLLIN
        self.poll.modify(self.fileno, type)

    def login(self, uid):
        self.uid = uid

    @property
    def logged(self):
        return self.uid != None
