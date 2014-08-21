# -*- coding: utf8 -*-
import json
from multiprocessing import Process
import urllib

from tornado.testing import AsyncHTTPTestCase
import zmq

from http_gate.app import create_application


CHANNEL = 'ipc:///tmp/test-http-gate'


class MockPerformer(Process):
    def run(self):
        context = zmq.Context(1)
        self.socket = context.socket(zmq.REP)
        self.socket.bind(CHANNEL)

        response = self.socket.recv_json()
        self.socket.send_json({'you': {'request': response}})

        self.socket.close()
        context.destroy()


class RequestTest(AsyncHTTPTestCase):
    def setUp(self):
        self.performer = MockPerformer()
        self.performer.start()
        super(RequestTest, self).setUp()
        self.command = {'command': 'hello'}

    def get_app(self):
        return create_application(CHANNEL, 'REQ')

    def handle_fetch(self, response):
        assert {'you': {'request': self.command}} == json.loads(response.body)
        self.stop()

    def test_request(self):
        self.http_client.fetch(
            self.get_url('/'),
            self.handle_fetch,
            method='POST',
            body=urllib.urlencode({'request': json.dumps(self.command)})
        )
        self.wait()