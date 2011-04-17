# coding: utf8

from listener import Listener
from sender import Sender
from talker import Talker
from test.test_case import TestCase
import time

class Zt_Talker_Base(TestCase):

    def tearDown(self):
        self.listener.close()
        self.sender.close()


class Zt_Talker_Threading(Zt_Talker_Base):

    def setUp(self):
        self.listener = Listener()
        self.listener.start()
        time.sleep(0.4)
        self.sender = Sender('', self.listener.port)

    def test_init(self):
        self.sender.connect()
        time.sleep(0.4)

        talker = self.listener.clients[0]
        self.assertTrue(isinstance(talker, Talker))
        self.wait_equal(talker.is_alive, True)

    def test_close(self):
        self.sender.connect()
        time.sleep(0.2)

        talker = self.listener.clients[0]
        self.assertTrue(isinstance(talker, Talker))
        self.wait_equal(talker.is_alive, True)
        talker.close()
        self.wait_equal(talker.is_alive, False)

    def test_client_out(self):
        self.sender.connect()
        time.sleep(0.2)

        talker = self.listener.clients[0]
        self.assertTrue(isinstance(talker, Talker))
        self.wait_equal(talker.is_alive, True)
        self.sender.close()
        self.wait_equal(talker.is_alive, False)


#class Zt_Talker(Zt_Talker_Base):
#
#    def setUp(self):
#        self.listener = Listener()
#        self.listener.start()
#        time.sleep(0.4)
#        self.sender = Sender('', self.listener.port)
#        self.data = {'param1':'param2', 'q':{'other':'me'},
#                     'command':'command'}
#
#    def test_command(self):
#        self.sender.send(self.data)
#        command = self.listener.mapper.get(self.data['command'])
#        self.assertEqual(self.sender.parse(), command(self.data))

