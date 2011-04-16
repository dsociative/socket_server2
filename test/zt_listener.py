# coding: utf8

from listener import Listener
from test.test_case import TestCase
import threading
import time


class Zt_Listener_Threading(TestCase):

    def setUp(self):
        self.listener = Listener()
        self.listener.start()

    def tearDown(self):
        try:
            self.listener.close()
        except:
            return

    def test_init(self):
        print threading.active_count()
        self.wait_equal(self.listener.is_alive, True)
        print threading.active_count()

    def test_close(self):
        print threading.active_count()
        self.listener.close()
        self.wait_equal(self.listener.is_alive, False)
        print threading.active_count()
