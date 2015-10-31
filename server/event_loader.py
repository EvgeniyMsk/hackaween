# -*- coding: utf-8 -*-

import requests
import time
import search_engine

class EventLoader(object):

    def __init__(self):
        self._se = search_engine.SearchEngine()
        pass

    def load(self):
        r = requests.get('http://kudago.com/public-api/v1/events/?fields=title,dates,id&page=1&page_size=100&actual_since={}&actual_until={}&location=spb&categories=concert'.format(time.time(), time.time() + 10713600))
        self._se.load(r.json())


if __name__ == "__main__":
    loader = EventLoader()
    loader.load()
    request = [{'artist': "Би-2", 'date': time.time()}]
    r = loader.search(request)
    for item in r:
        print "%s - %s" % (item['title'][0], item['date'][0])

