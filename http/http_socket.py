# coding: utf8
from base.common import command_error, init_logging
from threading import Thread
from tornado.escape import json_encode
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import url, RequestHandler, asynchronous
import json
import tornado.web


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

    def execute_cmd(self, cmd, params):
        try:
            msg = cmd(params)
            return msg
        except:
            command_error(self.client, params)


    @asynchronous
    def get(self):
        params = json.loads(self.get_argument('params'))
        command_id = params.get('command')

        msg = self.execute_cmd(self.authorization, params)
        if msg and msg.result != 1 or msg and params['command'] == self.authorization.name:
            return self.response(msg)

        command = self.mapper.get(command_id, self.client.uid)

        if not command:
            logging.warning('not found command %s' % command_id)
            return self.finish()

        command = command(self.client)
        msg = self.execute_cmd(command, params)
        if msg:
            self.response(msg)

    post = get

default_urls = [
    url(r'/', HttpSocketHandler),
    url(r'/crossdomain.xml', CrossDomainHandler),
    ]

app = tornado.web.Application()


class HttpSocket(Thread):

    def __init__(self, mapper, port=8888, urls={}, host=''):
        Thread.__init__(self)
        init_logging()

        for url_path, request_cls in urls.iteritems():
            default_urls.append(url(url_path, request_cls))

        Request.mapper = mapper
        self.port = port
        self.app = tornado.web.Application(default_urls)
        self.host = host

    def run(self):

        server = HTTPServer(self.app, self.host)

        server.bind(self.port)
        server.start(1)

        self.ioloop.start()

    def stop(self):
        self.ioloop.stop()

    @property
    def ioloop(self):
        return IOLoop.instance()
