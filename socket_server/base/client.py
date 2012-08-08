# coding: utf8

import select
from common import Common
from packer import Packer
from common import client_try
import logging


class Client(Common, Packer):

    def __init__(self, sock, addr, talker, uid=None):
        self.sock = sock
        self.talker = talker
        self.poll = talker.epoll

        self.uid = uid
        self.fileno = sock.fileno()
        self.queue = []
        self.peername = addr

        self.request = b''
        self.response = b''
        self.size = None

    def execute_cmd(self, params, cmd):
        try:
            cmd(self)(params)
        except:
            logging.error('%s %s' % (self.uid, cmd.name), exc_info=True)

    @client_try
    def recv(self):
        data = self.sock.recv(self.size or 4)
        if not data:
            self.unregister()
        else:
            if not self.size:
                self.size = self.packsize(data)
            else:
                self.request += data
                if len(self.request) >= self.size:
                    self.listen(self.unpack(self.size, self.request[:self.size]))
                    self.request = b''
                    self.size = None

    def listen(self, params):
        name = params.get('command')
        cmd = self.mapper.get(name, self.uid)

        if cmd:
            self.execute_cmd(params, cmd)

    def add_resp(self, resp):
        self.queue.insert(0, resp)
        self.refresh_state()

    def send(self):
        written = self.sock.send(self.response)
        self.response = self.response[written:]

    @client_try
    def reply(self):
        if not self.response:
            self.response = self.encode(self.queue.pop())

        self.send()

        if not self.response:
            self.response = b''
            self.refresh_state()

    def unregister(self):
        self.talker.unregister(self.fileno)

    def close(self):
        return self.sock.close()

    @property
    def has_reponse(self):
        return len(self.queue) > 0

    def modify(self, etype):
        try:
            self.poll.modify(self.fileno, etype)
        except:
            self.unregister()

    def refresh_state(self, etype=None):
        etype = select.EPOLLOUT if self.has_reponse else select.EPOLLIN
        self.modify(etype)

    def login(self, uid):
        self.uid = uid

    @property
    def logged(self):
        return self.uid != None
