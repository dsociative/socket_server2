# coding: utf8
from base.common import Common
from redis.client import Redis
import time


class BaseCommand(object):

    name = 'base.command'
    params = ()

    def __init__(self, client):
        self.msg = Message(self.name)
        self.client = client
        self.redis = Redis()

    def __call__(self, params):

        if not self.check_params(params):
            return

        params.pop('command')
        msg = self.execute(**params)
        Common.clients.send(msg.to_dict(), self.client.uid)

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
        self.time = int(time.mktime(time.localtime()))
        self.text = ''
        self.queue = {}
        self.uids = []

    def __setitem__(self, item, value):
        self.queue[item] = value

    def __getitem__(self, item):
        return self.queue.get(item)

    def error(self, text):
        self.result = 0
        self.text = text

    def fail_params(self, params):
        self.error('params not found: %s' % ', '.join(params))

    def to_dict(self):
        return {
                'result': self.result,
                'command': self.command,
                'time': self.time,
                'text': self.text,
                'queue': self.queue,
                'uids': self.uids,
                }
