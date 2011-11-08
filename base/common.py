# coding: utf8

import sys
import traceback
import logging
import select
import socket


def init_logging(level='DEBUG'):
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level = logging.WARNING

    logging.basicConfig(format=format, level=level)

def trace():
    traceback.print_exc(file=sys.stderr)

def command_error(client, params):
    logging.warning("uid:%s %s" % (client.uid, params))
    trace()

class Common(object):

    mapper = None

def client_try(f):

    def w(self, *args, **kw):
        try:
            return f(self, *args, **kw)
        except socket.error:
            self.modify(select.EPOLLERR)
        except:
            logging.error('%s %s' % (self.uid, f.func_name))
            self.modify(select.EPOLLERR)
            trace()

    return w
