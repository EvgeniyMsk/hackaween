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
        r = requests.get('http://kudago.com/public-api/v1/events/?fields=title,dates,id,place,images,description&page=1&page_size=100&actual_since={}&actual_until={}&location=spb&categories=concert'.format(time.time(), time.time() + 10713600))
        self._se.load(r.json())


if __name__ == "__main__":
    se = search_engine.SearchEngine()
    se.delete_indexes()
    se.create_index('mytemp')
    ev = EventLoader(se)
    ev.load()

