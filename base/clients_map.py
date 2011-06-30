# coding: utf8

class ClientsMap(object):

    def __init__(self, talker):
        self.talker = talker

        self.clients = {}
        self.users = {}

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

    def add_user(self, client, uid):
        existing_client = self.users.get(uid)
        if existing_client:
            self.talker.unregister(existing_client.fileno)

        client.uid = uid
        self.users[client.uid] = client

    def send(self, uid, msg):
        client = self.users.get(uid)
        if client:
            client.add_resp(msg)

    def __len__(self):
        return len(self.clients)
