import json

from urllib2 import urlopen, Request

from server.initializer import Initializer

if __name__ == "__main__":

    context = Initializer.get_context()
    http_cfg = context.get_http_cfg()
    url = "{}:{}".format(http_cfg["host"], http_cfg["port"])

    with open("music.json") as fd:
        music = fd.read()

    request = Request(url, music)
    response = urlopen(request)