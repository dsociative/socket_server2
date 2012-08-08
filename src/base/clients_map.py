# coding: utf8

from util.subscriber import Subscriber


class Subsciber(Subscriber):

    def __init__(self, clients_map, channel='messaging'):
        self.clients = clients_map
        Subscriber.__init__(self, clients_map.redis, channel)

    def parse(self, data):
        return eval(data)

    def process(self, message):
        uids = message.pop('uids')
        self.clients.queue(uids, message)


class ClientsMap(object):

    def __init__(self, talker, redis, db_channel):
        self.talker = talker

        self.clients = {}
        self.users = {}
        self.redis = redis
        self.channel = db_channel
        self.channel_disconnect = '_'.join((db_channel, 'disconnect'))

        self.subcriber = Subsciber(self, self.channel)
        self.subcriber.start()

    def __setitem__(self, fileno, client):
        self.clients[fileno] = client

    def __getitem__(self, fileno):
        return self.get(fileno)

    def get(self, fileno):
        return self.clients.get(fileno)

    def __delitem__(self, fileno):
        client = self.clients[fileno]
        if client.logged:
            self.redis.publish(self.channel_disconnect, client.uid)
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
