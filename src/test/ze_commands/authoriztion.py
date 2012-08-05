# coding: utf8

from test.ze_commands.base_command import BaseCommand


class Authorization(BaseCommand):

    name = 'user.authorization'
    params = 'uid', 'auth_key'

    def execute(self, uid, auth_key):
        self.client.login(uid)

        return self.msg
