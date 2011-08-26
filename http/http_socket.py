# coding: utf8
from tornado.escape import json_encode
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import url, RequestHandler, asynchronous
import json
import logging
import thread
import tornado.web\

from threading import Thread


CROSSDOMAIN = """<?xml version="1.0"?>
<cross-domain-policy>
  <allow-access-from domain="*" />
</cross-domain-policy>"""

class Request(RequestHandler):

    mapper = None
    client = None

class CrossDomainHandler(Request):

    def get(self):
        self.finish(CROSSDOMAIN)

class HttpUserSocket(object):

    def __init__(self, uid):
        self.uid = uid

    def sendCmd(self, msg):
        self.msg = msg
        return

class WebClient(object):

    def __init__(self):
        self.uid = None

class HttpSocketHandler(Request):

    def initialize(self):
        self.client = WebClient()

    def response(self, msg):
        self.finish(json_encode(msg.to_dict()))

    @property
    def authorization(self):
        return self.mapper.auth(self.client)

    def get(self):
        params = json.loads(self.get_argument('params'))
        command_id = params.get('command')

        msg = self.authorization(params)
        if msg.result != 1 or params['command'] == self.authorization.name:
            return self.response(msg)

        command = self.mapper.get(command_id, self.client.uid)

        if not command:
            logging.warning('not found command %s' % command_id)
            return self.finish()

        command = command(self.client)
        self.response(command(params))

    post = get


app = tornado.web.Application([
    url(r'/', HttpSocketHandler),
    url(r'/crossdomain.xml', CrossDomainHandler),
    ])


class HttpSocket(Thread):

    def __init__(self, mapper, port=8888):
        Thread.__init__(self)

        Request.mapper = mapper
        self.server = HTTPServer(app)

    def run(self):
        self.server.bind(port)
        self.server.start(1)
        self.ioloop.start()

    def stop(self):
        self.ioloop.stop()

    @property
    def ioloop(self):
        return IOLoop.instance()
