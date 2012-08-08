# coding: utf8

from socket_server.client.simple_client import SimpleClient


class TestClient(SimpleClient):

    disconnected = []

    def disconnect(self, id):
        self.disconnected.append(id)
