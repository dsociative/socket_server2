# coding: utf8

from redis.client import Redis
from socket_server.test import TestCase
from socket_server.util.subscriber import Subscriber


class SubscriberTest(TestCase):

    def test_close(self):
        subscriber = Subscriber(Redis(), 'test_channel')
        self.assertEqual(subscriber.is_alive(), False)
        subscriber.start()
        self.assertEqual(subscriber.is_alive(), True)
        self.wait_equal(subscriber.pubsub.patterns, set(['test_channel']))
        subscriber.stop()
        self.wait_equal(subscriber.is_alive, False)
