# coding: utf8

from redis import Redis
from threading import Thread
from random import random

def ismsg(d):
    return d['type'] == 'pmessage'

def isdie(d):
    return d['data'] == 'die'

class Subsciber(Thread):

    def __init__(self, clients_map, channel='messaging'):
        Thread.__init__(self)

        self.clients = clients_map
        self.channel = channel

        self.pubsub = clients_map.redis.pubsub()
        self.closemsg = 'close_%s' % random()

    def isclose(self, d):
        return d['data'] == self.closemsg

    def run(self):
        self.pubsub.psubscribe(self.channel)

        for d in self.pubsub.listen():
            if ismsg(d):

                if self.isclose(d):
                    break
                else:
                    msg = eval(d['data'])
                    uids = msg.pop('uids')
                    self.clients.queue(uids, msg)

        return self

    def stop(self):
        self.clients.redis.publish(self.channel, self.closemsg)


class ClientsMap(object):

    def __init__(self, talker, config):
        self.talker = talker
        self.clients = {}
        self.users = {}

    def __setitem__(self, fileno, client):
        self.clients[fileno] = client

    def __getitem__(self, fileno):
        return self.get(fileno)

    def get(self, fileno):
        return self.clients.get(fileno)

    def __delitem__(self, fileno):
        client = self.clients[fileno]
        if client.logged:
            del self.users[client.uid]
        del self.clients[fileno]

    def queue(self, uids, msg):
        for uid in uids:
            client = self.users.get(uid)
            if client:
                client.add_resp(msg)

    def add_user(self, client, uid):
        existing_client = self.users.get(uid)
        if existing_client:
            self.talker.unregister(existing_client.fileno)

        client.uid = uid
        self.users[client.uid] = client

    def send(self, msg, *uids):
        msg['uids'] = uids
        self.redis.publish(self.channel, msg)

    def __len__(self):
        return len(self.clients)
