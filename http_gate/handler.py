# -*- coding: utf8 -*-
from tornado.concurrent import return_future
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def post(self, *args, **kwargs):
        self.settings['socket'].send_string(self.get_argument('request'))
        self.finish(self.settings['socket'].recv())

    @return_future
    def get_response(self, callback):
        callback(self.settings['socket'].recv())
