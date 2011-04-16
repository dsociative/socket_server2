# coding: utf8

from common import Common
from packer import Packer
from threading import Thread

class Talker(Common, Packer, Thread):

    listener = True
    time_out = 5

    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket
        self.socket.settimeout(self.time_out)

    def execute_cmd(self, params):
        command_id = params.get('command')
        if command_id:
            command = self.mapper.get(command_id)
            if command:
                return command(params)

    def response(self, params):
        data = self.encode(params)
        return self.socket.send(self.pack(data))

    def run(self):
        while self.listener and self.socket:
            size = self.packsize(self.socket.recv(self.SBIN_SIZE))
            if size:
                data = self.unpack(size, self.socket.recv(size))
                resp = self.execute_cmd(self.decode(data))
                if resp:
                    self.response(resp)

    def close(self):
        self.socket.close()
