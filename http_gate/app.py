# -*- coding: utf8 -*-
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application, url
import zmq

from http_gate.handler import IndexHandler


define(
    'channel',
    default='ipc:///tmp/gate',
    help='ZMQ channel where to send received messages'
)
define(
    'socket_type',
    default='REQ',
    help='ZMQ socket type - REQ, PULL, PUB, etc'
)
define('port', default=8888)
define('host', default='')


def init_socket(channel, socket_type):
    context = zmq.Context(1)
    socket = context.socket(getattr(zmq, socket_type))
    socket.connect(channel)
    return socket


def create_application(channel, socket_type):
    return Application(
        [url('/', IndexHandler)], socket=init_socket(channel, socket_type),
    )


def start(socket_type, channel, host, port):
    application = create_application(channel, socket_type)
    application.listen(port, address=host)
    IOLoop.instance().start()


def main():
    options.parse_command_line()

    start(options.socket_type, options.channel, options.host, options.port)


if __name__ == "__main__":
    main()