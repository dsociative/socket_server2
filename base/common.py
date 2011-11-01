# coding: utf8

import sys
import traceback
import logging
import select


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
    policy_xml = '''<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
<allow-access-from domain="*" to-ports="*" secure="false" />
</cross-domain-policy>'''


def client_try(f):

    def w(self, *args, **kw):
        try:
            return f(self, *args, **kw)
        except:
            logging.error('%s %s' % (self.uid, f.func_name))
            self.modify(select.EPOLLERR)
            trace()

    return w
