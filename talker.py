# coding: utf8

from common import Common
from packer import Packer
from threading import Thread, active_count

class Talker(Common, Packer, Thread):

    listener = True
    time_out = 5

    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket
        self.socket.settimeout(self.time_out)
        self.policy_requested = False

    def execute_cmd(self, params):
        print active_count()
        command_id = params.get('command')
        if command_id:
            command = self.mapper.get(command_id)
            if command:
                return command(params)

    def response(self, params):
        data = self.encode(params)
        return self.send(self.pack(data))

    def send(self, data):
        return self.socket.sendall(data + '\0')

    def run(self):
        while self.listener and self.socket:
            t = self.socket.recv(self.SBIN_SIZE)
            size = self.packsize(t)
            if size:
                data = self.unpack(size, self.socket.recv(size + 1))
                resp = self.execute_cmd(self.decode(data))
                self.response(resp)

    def request_policy(self):
        self.policy_requested = True
        return self.socket.send(self.policy_xml)

    def close(self):
        self.socket.close()
