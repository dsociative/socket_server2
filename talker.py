# coding: utf8

from common import Common
from packer import Packer
from threading import Thread
import socket

class Talker(Common, Packer, Thread):

    listener = True
    time_out = 5
    commands = 0

    def __init__(self, socket):
        Thread.__init__(self)
        print 'TALKER INIT %s' % socket
        self.socket = socket
        self.socket.settimeout(self.time_out)
        self.policy_requested = False

    def execute_cmd(self, params):
        Talker.commands += 1
        print self.commands
        command_id = params.get('command')
        if command_id:
            command = self.mapper.get(command_id)
            if command:
                return command(params)

    def response(self, params):
        data = self.encode({'q':'qwe'})
        binary = self.pack(data)
        return self.socket.sendall(binary + '\0')

    def run(self):
        while self.listener and self.socket:
#            print self.socket.recv(0x10000, socket.MSG_WAITALL)
            t = self.socket.recv(self.SBIN_SIZE)
            size = self.packsize(t)
            if size:
                data = self.unpack(size, self.socket.recv(size))
                resp = self.execute_cmd(self.decode(data))
                self.response(resp)

    def request_policy(self):
        self.policy_requested = True
        print 'CROSSDOMAIN ALERT'
        return self.socket.send(self.policy_xml)

    def close(self):
        self.socket.close()
