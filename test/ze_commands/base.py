# coding: utf8
import time


class BaseCommand(object):

    name = 'base.command'
    params = ()

    def __init__(self, client):
        self.msg = Message(self.name)
        self.client = client

    def __call__(self, params):

        if not self.check_params(params):
            return

        params.pop('command')
        return self.execute(**params)

    def check_params(self, real):
        fail = []
        for expected in self.params:
            if not expected in real:
                fail.append(expected)

        if fail:
            self.msg.fail_params(fail)
            return False
        else:
            return True



class Message(object):

    def __init__(self, command):
        self.result = 1
        self.command = command
        self.time = int (time.mktime(time.localtime()))
        self.result_text = ''
        self.response = {}

    def __setitem__(self, item, value):
        self.response[item] = value

    def __getitem__(self, item):
        return self.response.get(item)

    def error(self, text):
        self.result = 0
        self.text = text

    def fail_params(self, params):
        self.error('params not found: %s' % ', '.join(params))

    def to_dict(self):
        dict = {
                'result': self.result,
                'command': self.command,
                'time': self.time,
                'result_text': self.result_text,
                'response': self.response
                }
        return dict
