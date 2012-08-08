# coding: utf8

from random import random
from threading import Thread


def ismsg(d):
    return d['type'] == 'pmessage'


class Subscriber(Thread):

    def __init__(self, redis, channel):
        Thread.__init__(self)
        self.redis = redis
        self.channel = channel
        self.pubsub = redis.pubsub()
        self.closemsg = 'close_%s' % random()
        self.pubsub.psubscribe(self.channel)

    def isclose(self, d):
        return d['data'] == self.closemsg

    def parse(self, data):
        return data

    def process(self, message):
        pass

    def run(self):
        for d in self.pubsub.listen():
            if ismsg(d):

                if self.isclose(d):
                    self.pubsub.reset()
                    break
                else:
                    self.process(self.parse(d['data']))

        return self

    def stop(self):
        self.redis.publish(self.channel, self.closemsg)
