# coding: utf8
from base.common import command_error
from threading import Thread
from tornado.escape import json_encode
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import url, RequestHandler, asynchronous
import json
import tornado.web
import logging


CROSSDOMAIN = """<?xml version="1.0"?>
<cross-domain-policy>
  <allow-access-from domain="*" />
</cross-domain-policy>"""

store = None

class CrossDomainHandler(RequestHandler):

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

class HttpSocketHandler(RequestHandler):

    def initialize(self):
        self.client = WebClient()
        self.mapper = self.application.mapper

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


    def isauth_cmd(self, params, command_id):
        return command_id == self.authorization.name


    @asynchronous
    def get(self):
        params = json.loads(self.get_argument('params'))
        command_id = params.get('command')

        if not self.isauth_cmd(params, command_id):
            if not self.auth_func(self.client, params):
                return self.response({'result':0, 'result_text':'auth failed'})

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

    def __init__(self, mapper, auth_func, port=8888, urls={}, host=''):
        Thread.__init__(self)
        RequestHandler.auth_func = auth_func

        for url_path, request_cls in urls.iteritems():
            default_urls.append(url(url_path, request_cls))

        self.port = port
        self.app = tornado.web.Application(default_urls)
        self.app.mapper = mapper
        self.host = host

    def run(self):

        server = HTTPServer(self.app)

        server.bind(self.port, self.host)
        server.start(1)

        self.ioloop.start()

    def stop(self):
        self.ioloop.stop()

    @property
    def ioloop(self):
        return IOLoop.instance()
