# coding: utf8

import sys
import traceback
import logging
import select
import socket


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
            err_str = '%s %s %s' % (self.uid, f.im_class.__name__, f.func_name)
            logging.error(err_str, exc_info=True)
            self.modify(select.EPOLLERR)

    return w
