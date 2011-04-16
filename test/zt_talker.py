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
        self.sender.close()

    def test_command(self):
        self.sender.send(self.data)
        command = self.listener.mapper.get(self.data['command'])
        self.assertEqual(self.sender.parse(), command(self.data))

