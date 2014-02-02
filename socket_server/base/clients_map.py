# coding: utf8
import logging


class ClientsMap(object):

    def __init__(self):
        self.by_fileno = {}
        self.by_cid = {}

    def __setitem__(self, fileno, client):
        self.by_fileno[fileno] = client
        self.by_cid[client.id] = client

    def get(self, fileno):
        return self.by_fileno.get(fileno)

    def __delitem__(self, fileno):
        client = self.by_fileno.pop(fileno, None)
        if client:
            del self.by_cid[client.id]
        else:
            logging.warning('client not found in by_fileno')

    def queue(self, cids, msg):
        for uid in cids:
            client = self.by_cid.get(uid)
            if client:
                client.add_resp(msg)

    def __len__(self):
        return len(self.by_fileno)
