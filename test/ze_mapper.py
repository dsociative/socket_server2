from test.ze_commands.authoriztion import Authorization


class Mapper(object):

    auth = Authorization,
    command = ()

    def __init__(self):
        self.namespace = {}
        for cmd in self.auth:
            self.namespace[cmd.name] = cmd

    def get(self, name):
        cmd = self.namespace.get(name)
        return cmd
