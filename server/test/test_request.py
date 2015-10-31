# -*- coding: utf-8 -*-

import json
import logging

from urllib2 import urlopen, Request

from server.initializer import Initializer

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    context = Initializer.get_context()
    http_cfg = context.get_http_cfg()
    url = "http://{}:{}".format(http_cfg["host"], http_cfg["port"])

    with open("music.json") as fd:
        music = fd.read()#.decode("cp1251", "ignore").encode("utf-8", "ignore")

    request = Request(url, music)
    response = urlopen(request)
    str_response = response.read()
    logging.debug("Response: {}".format(str_response))
    events = json.loads(str_response)
    print events
    # for event in events["eventsResponse"]:
    #     try:
    #         print "title: {}".format(event["title"]).decode("cp1251", "ignore")
    #     except Exception as exc:
    #         print "ERROR: {}".format(str(exc))