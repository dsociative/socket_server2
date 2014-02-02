# coding: utf8
import logging

from socket_server.client.simple_client import SimpleClient


class TestClient(SimpleClient):

    disconnected = []

    def disconnect(self, id):
        self.disconnected.append(id)

    def listen(self, message):
        self.add_resp('hello')
