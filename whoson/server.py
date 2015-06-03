#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from json import loads, dumps
from datetime import datetime
import base64

from cow.server import Server
import tornado.web
import tornado.websocket
from tornado.httpclient import AsyncHTTPClient
from tornado_redis_sentinel import SentinelClient

from whoson import __version__


def main():
    WhosOnApiServer.run()


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(__version__)


class SubWebSocket(tornado.websocket.WebSocketHandler):
    def open(self, url):
        self.url = url
        self.application.pubsub.subscribe(self.get_key(), callback=self.handle_redis_message)

    def handle_redis_message(self, message):
        print "SENT Message %s" % message

        if message[0] != 'message':
            return

        self.write_message(message[2])

    def on_message(self, message):
        print "RECEIVED Message %s" % message

        if message[0] != '{':
            return

        obj = loads(message)

        self.application.redis.publish(self.get_key(), dumps({
            "user": obj['user'],
            "url": obj['url']
        }))

    def on_close(self):
        self.application.pubsub.unsubscribe(self.get_key())
        self.application.pubsub._sub_callback = None

    def get_key(self):
        return base64.b64encode(self.url.rstrip('/'))


class WhosOnApiServer(Server):
    def __init__(self, debug=None, *args, **kw):
        super(WhosOnApiServer, self).__init__(*args, **kw)

        self.force_debug = debug

    def get_extra_server_parameters(self):
        return {
            'no_keep_alive': False
        }

    def initialize_app(self, *args, **kw):
        super(WhosOnApiServer, self).initialize_app(*args, **kw)

        if self.force_debug is not None:
            self.debug = self.force_debug

    def get_handlers(self):
        handlers = [
            ('/version/?', VersionHandler),
            ('/subscribe/(.+?)/?', SubWebSocket),
        ]

        return tuple(handlers)

    def get_plugins(self):
        return []

    def connect(self):
        sentinel_hosts = self.application.config.get('SENTINEL_HOSTS')
        sentinel_hosts = loads(sentinel_hosts)

        self.application.redis.connect(
            sentinels=sentinel_hosts,
            master_name=self.application.config['REDIS_MASTER']
        )

        self.application.pubsub.connect(
            sentinels=sentinel_hosts,
            master_name=self.application.config['REDIS_MASTER']
        )


    def after_start(self, io_loop):
        self.application.redis = SentinelClient(io_loop=self.application.io_loop, disconnect_callback=self.on_disconnect)
        self.application.pubsub = SentinelClient(io_loop=self.application.io_loop, disconnect_callback=self.on_disconnect)
        self.connect()

    def on_disconnect(self, status):
        self.connect()


if __name__ == '__main__':
    main()
