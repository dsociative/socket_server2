# coding: utf8

from sender import Sender
from threading import Thread
import signal
import time

def timer(diff=None):
    current = time.time()

    if not diff:
        return current
    else:
        return current - diff

class Client(Thread):

    delay = 0
    working = False

    param = {"command": "user.authorization",
             "uid": "6104128459101111038",
             "auth_key": "599bf8e08afc3003d0db1a7f048eee49",
             "get_data":1}

    expected = {'command':'ok'}

    timings = []
    messages = 0
    count = 0
    error = 0

    def connect(self):
        if self.working:
            Client.count += 1
            return Sender('', 8885).connect()

    def do_command(self, sender):
        time = timer()
        sender = self.connect()
        sender.send(self.param)
        resp = sender.parse()
        sender.close()

        Client.messages += 1
        return timer(time)

    def run(self):
        sender = self.connect()

        while Client.working:
            Client.timings.append(self.do_command(sender))
            time.sleep(self.delay)
        else:
            sender.close()



if __name__ == '__main__':

    start_time = timer()
    workers = 1

    def quit(q, w):
        Client.working = False
        duration = timer(start_time)

        print 'clients %s' % Client.count
        print 'delay %f sec' % (Client.delay)
        print 'messages %s' % Client.messages
        print 'connection error %s' % Client.error

        print 'min timing %s' % min(Client.timings)
        print 'max timing %s' % max(Client.timings)
        print 'duration %s commands %s per sec' % (duration,
                                                   Client.messages / duration)

    signal.signal(signal.SIGINT, quit)
    Client.working = True

    for i in xrange(workers):
        t = Client()
        t.setDaemon(True)
        t.start()
        print 'start %s' % i


    while Client.working:
        time.sleep(1)

