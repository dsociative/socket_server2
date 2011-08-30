# coding:
from base.common import trace, command_error
from common import Common
from packer import Packer
import select

class Client(Common, Packer):

    def __init__(self, sock, addr, talker, uid=None):
        self.sock = sock

        self.talker = talker
        self.poll = talker.epoll

        self.uid = uid
        self.fileno = sock.fileno()
        self.response = []
        self.peername = addr

    def execute_cmd(self, params, cmd):
        try:
            resp = cmd(self)(params)
            return self.add_resp(resp)
        except:
            command_error(self, params)
            return None

    def recv(self):

        try:
            data = self.sock.recv(1024)
            if not data:
                self.unregister()
            else:
                return self.listen(self.decode(data))

        except Exception, _:
            trace()
            self.unregister()


    def listen(self, params):

        name = params.get('command')
        cmd = self.mapper.get(name, self.uid)


        if cmd:
            self.execute_cmd(params, cmd)

    def add_resp(self, resp):
        self.response.insert(0, resp)
        self.refresh_state()

    def reply(self):
        resp = self.response.pop()
        self.sock.send(self.encode(resp))
        self.refresh_state()

    def unregister(self):
        self.talker.unregister(self.fileno)

    def close(self):
        return self.sock.close()

    @property
    def has_reponse(self):
        return len(self.response) > 0

    def refresh_state(self):
        try:
            type = select.EPOLLOUT if self.has_reponse else select.EPOLLIN
            self.poll.modify(self.fileno, type)
        except:
            trace()

    def login(self, uid):
        self.uid = uid

    @property
    def logged(self):
        return self.uid != None
