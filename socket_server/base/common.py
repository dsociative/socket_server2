# coding: utf8

import sys
import traceback
import logging
import socket


def trace():
    traceback.print_exc(file=sys.stderr)


def command_error(client, params):
    logging.warning("uid:%s %s" % (client.uid, params))
    trace()


class Common(object):

    mapper = None

    @classmethod
    def set_mapper(cls, mapper, clients):
        cls.mapper = mapper
        cls.clients = clients


def client_try(f):

    def w(self, *args, **kw):
        try:
            return f(self, *args, **kw)
        except socket.error:
            pass
        except:
            logging.error('%s %s' % (self.id, f.func_name), exc_info=True)

        self.hung_up()

    return w
