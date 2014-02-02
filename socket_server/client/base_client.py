# coding: utf8
import socket

from socket_server.base.common import Common, client_try
from socket_server.base.packer import Packer
import select


class BaseClient(Common, Packer):
    count = 0

    def __init__(self, sock, addr, talker):
        self.id = self.__get_id()

        self.sock = sock
        self.talker = talker

        self.fileno = sock.fileno()
        self.queue = []
        self.peername = addr

        self.request = b''
        self.response = b''
        self.size = None

    def __get_id(self):
        BaseClient.count += 1
        return self.count

    @client_try
    def recv(self):
        data = self.sock.recv(self.size or 4)
        if not data:
            self.hung_up()
        else:
            if not self.size:
                self.size = self.packsize(data)
            else:
                self.request += data
                if len(self.request) >= self.size:
                    self.listen(
                        self.unpack(self.size, self.request[:self.size])
                    )
                    self.request = b''
                    self.size = None

    def listen(self, request):
        """ What to do with request? """

    def add_resp(self, resp):
        self.queue.insert(0, resp)
        self.refresh_state()

    def send(self):
        written = self.sock.send(self.response)
        self.response = self.response[written:]

    @client_try
    def reply(self):
        if not self.response:
            if self.has_reponse:
                self.response = self.encode(self.queue.pop())
            else:
                return self.refresh_state()

        self.send()

        if not self.response:
            self.response = b''
            self.refresh_state()

    def disconnect(self, cid):
        raise Exception('template method')

    def close(self):
        self.sock.close()
        self.disconnect(self.id)

    @property
    def has_reponse(self):
        return len(self.queue) > 0

    def modify(self, etype):
        self.talker.modify(self.fileno, etype)

    def hung_up(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except socket.error:
            self.talker.unregister(self.fileno)
        else:
            self.modify(select.EPOLLHUP)

    def refresh_state(self):
        etype = select.EPOLLOUT if self.has_reponse else select.EPOLLIN
        self.modify(etype)
