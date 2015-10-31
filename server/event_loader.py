# -*- coding: utf-8 -*-

import requests
import time
import search_engine
import initializer
import event_adviser

class EventLoader(object):

    def __init__(self, se):
        self._se = se
        pass

    def load(self):
        r = requests.get('http://kudago.com/public-api/v1/events/?fields=title,dates,id&page=1&page_size=100&actual_since={}&actual_until={}&location=spb&categories=concert'.format(time.time(), time.time() + 10713600))
        self._se.load(r.json())


if __name__ == "__main__":
    initil = initializer.Initializer()
    el = EventLoader(initil.getSE())
    # el.load()
    ed = event_adviser.EventAdviser(initil.getSE())
    request = [{'artist': "Би-2", 'date': time.time()}]
    r = ed.search(request)
    for item in r:
        print "%s - %s" % (item['title'][0], item['date'][0])

