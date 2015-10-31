# -*- coding: utf-8 -*-

import os
import textwrap
import json
import logging

import requests
import time
import search_engine

from initializer import Initializer

class EventLoader(object):

    _MAX_DEPTH = 5

    def __init__(self, se, kudago_cfg):
        self._se = se

        self._kudago_fields = ",".join(kudago_cfg["fields"])
        self._kudago_expand = ",".join(kudago_cfg["expand"])
        pass

    def load(self):
        for root, dir, files in os.walk("test"):
            for fn in files:
                if "kudago" in fn:
                    fn = os.path.join(root, fn)
                    logging.debug("Load events from file {} to index".format(fn))
                    with open(fn) as fd:
                        events = json.load(fd)
                        self._se.load(events)

    def http_load(self):
        now = time.time()
        until = now + 10713600
        url = textwrap.dedent(
            """
            http://kudago.com/public-api/v1/events/?
            fields={fields}&expand={expand}&page=1&page_size=100&
            actual_since={since}&actual_until={until}&
            location=spb&categories=concert
            """\
            .format(fields=self._kudago_fields, expand=self._kudago_expand, since=now, until=until))
        url = "".join(url.splitlines())

        self._deep_load(url, 1)

    def _deep_load(self, url, depth):
        if depth > self._MAX_DEPTH:
            return

        logging.debug("Send request to kudago: {}".format(url))
        events = requests.get(url).json()
        next_url = events["next"]
        self._on_http_load(events, depth)
        self._deep_load(next_url, depth+1)

    def _on_http_load(self, events, page):
        name = "test/kudago{}.json".format(str(page))
        logging.debug("Save events to {}".format(name))
        with open(name, "w") as fd:
            json.dump(events, fd)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    context = Initializer.get_context()
    se = context.get_se()
    kudago_cfg = context.get_kudago_cfg()
    es_cfg = context.get_es_cfg()

    loader = EventLoader(se, kudago_cfg)

    # update from kudago
    #loader.http_load()

    # load files to index
    se.delete_index(es_cfg["index"])
    se.create_index(es_cfg)
    loader.load()

