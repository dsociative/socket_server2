# coding: utf8

from listener import Listener
from test.test_case import TestCase
import threading
import time


class Zt_Listener_Threading(TestCase):

    def setUp(self):
        self.listener = Listener()

    def tearDown(self):
        self.listener.close()

    def test_init(self):
        active_threads = threading.active_count()
        self.listener.start()
        self.assertEqual(threading.active_count(), active_threads + 1)
        self.listener.close()
        time.sleep(1)

    def test_close(self):
        active_threads = threading.active_count()
        self.listener.start()
        self.listener.close()
        time.sleep(1)
        self.assertEqual(threading.active_count(), active_threads)
