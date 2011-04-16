# coding: utf8

from common import Common
from packer import Packer
from threading import Thread, active_count
import logging

def log_debug(f):

    def wrapper(obj, *args, **kwargs):
        logging.debug('%s - %s' % (obj, f.func_name))

        return f(obj, *args, **kwargs)

    return wrapper

class Talker(Common, Packer, Thread):

    time_out = 5

    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket
        self.socket.settimeout(self.time_out)
        self.policy_requested = False

    def __repr__(self):
        return '<Talker %s>' % self.name

    def execute_cmd(self, params):
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

    def recive(self, count):
        try:
            return self.socket.recv(count)
        except socket.time_out:
            logging.debug('%s time out' % self.name)
            return self.close()

    @log_debug
    def run(self):
        self.status = True

        while self.status:
            size = self.packsize(self.recive(self.SBIN_SIZE))
            if size:
                data = self.unpack(size, self.socket.recv(size + 1))
                resp = self.execute_cmd(self.decode(data))
                self.response(resp)

        logging.debug('%s exit' % self.name)


    @log_debug
    def close(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error, err:
            logging.warning(err)
        self.socket.close()
        self.status = False
