# -*- coding: utf8 -*-
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def post(self, *args, **kwargs):
        self.settings['socket'].send_string(self.get_argument('request'))
        self.finish(self.settings['socket'].recv())
