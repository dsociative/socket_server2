# coding: utf8

from base.common import Common
from test.ze_commands.base_command import BaseCommand


class Authorization(BaseCommand):

    name = 'user.authorization'
    params = 'uid', 'auth_key'

    def execute(self, uid, auth_key):
        Common.clients.add_user(self.client, uid)
        return self.msg
