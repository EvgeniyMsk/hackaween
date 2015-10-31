# -*- coding: utf-8 -*-

class EventAdviser(object):

    def __init__(self, se, artist_ranker, event_ranker):
        self._se = se
        self._artist_ranker = artist_ranker
        self._event_ranker = event_ranker
        pass

    def search(self, requests):
        top = self._artist_ranker.rank(requests, 50)
        events =  self._se.search(requests)
        return self._event_ranker.rank(events, top)
