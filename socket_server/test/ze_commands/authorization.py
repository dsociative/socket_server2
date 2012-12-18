# coding: utf8

from socket_server.base.common import Common
from socket_server.test.base_command import BaseCommand


class Authorization(BaseCommand):

    name = 'user.authorization'
    params = 'uid', 'auth_key'

    def execute(self, uid, auth_key):
        Common.clients.add_user(self.client, uid)
        return self.msg


class TrashClass(object):
    """
    For Tests
    """
    pass