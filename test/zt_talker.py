# coding: utf8

from listener import Listener
from sender import Sender
from test.test_case import TestCase
import time
import pyamf

class Zt_Talker(TestCase):

    def setUp(self):
        self.listener = Listener()
        self.listener.start()
        time.sleep(0.4)
        self.sender = Sender('', self.listener.port)
        self.data = {'param1':'param2', 'q':{'other':'me'},
                     'command':'command'}

    def tearDown(self):
        self.listener.close()

    def test_policy_xml(self):
        recv = self.sender.send(self.data)
        self.assertEqual(recv, self.listener.policy_xml + '\0')

        self.sender.send(self.data)
        recv = self.sender.send(self.data)
        obj = self.sender.decode(recv)
        self.assertEqual(recv, self.listener.policy_xml + '\0')

