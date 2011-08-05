# coding: utf8

from redis import Redis
from threading import Thread

def ismsg(d):
    return d['type'] == 'message'

class Subsciber(Thread):

    def __init__(self, clients_map, channel='messaging'):
        Thread.__init__(self)

        self.redis = Redis()
        self.clients = clients_map
        self.channel = channel
        self.listener = self.redis.listen()

    def run(self):
        self.redis.subscribe(self.channel)

        for d in self.listener:
            print d
            if ismsg(d):
                msg = eval(d['data'])
                uids = msg.pop('uids')
                self.clients.response(uids, msg)

        return self

    def stop(self):
        self.listener.close()


class ClientsMap(object):

    def __init__(self, talker, config):
        self.talker = talker

        self.clients = {}
        self.users = {}
        self.redis = Redis()
        self.channel = config.get('sockets', 'db_channel')

        self.subcriber = Subsciber(self, self.channel)
        self.subcriber.start()

    def __setitem__(self, fileno, client):
        self.clients[fileno] = client

    def __getitem__(self, fileno):
        return self.clients.get(fileno)

    def get(self, fileno):
        return self[fileno]


    def __delitem__(self, fileno):
        client = self.clients[fileno]
        if client.logged:
            del self.users[client.uid]
        del self.clients[fileno]

    def response(self, uids, msg):
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
