# coding: utf8


class ClientsMap(object):

    def __init__(self, talker):
        self.talker = talker
        self.clients = {}
        self.users = {}

    def __setitem__(self, fileno, client):
        self.clients[fileno] = client
        self.users[client.id] = client

    def __getitem__(self, fileno):
        return self.get(fileno)

    def get(self, fileno):
        return self.clients.get(fileno)

    def __delitem__(self, fileno):
        del self.users[self.clients[fileno].id]
        del self.clients[fileno]

    def queue(self, uids, msg):
        for uid in uids:
            client = self.users.get(uid)
            if client:
                client.add_resp(msg)

    def send(self, msg, *uids):
        msg['uids'] = uids

    def __len__(self):
        return len(self.clients)
