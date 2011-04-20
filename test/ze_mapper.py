from test.ze_commands.authoriztion import Authorization


class Mapper(object):

    auth = Authorization,
    command = ()

    def __init__(self):
        self.auth_space = {}
        self.cmd_space = {}

        for cmd in self.auth:
            self.auth_space[cmd.name] = cmd
        for cmd in self.command:
            self.cmd_space[cmd.name] = cmd

    def get(self, name, auth=False):
        if not auth:
            return self.auth_space.get(name)
        else:
            return self.cmd_space.get(name)
