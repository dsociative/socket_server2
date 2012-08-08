# coding: utf8

from socket_server.client.base_client import BaseClient
import logging


class SimpleClient(BaseClient):

    def execute_cmd(self, params, cmd):
        try:
            cmd(self)(params)
        except:
            logging.error('%s %s' % (self.uid, cmd.name), exc_info=True)

    def listen(self, params):
        name = params.get('command')
        cmd = self.mapper.get(name, self.uid)

        if cmd:
            self.execute_cmd(params, cmd)
