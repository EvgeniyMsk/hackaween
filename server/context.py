# -*- coding: utf-8 -*-

class Context(object):

    def __init__(self, se, artist_ranker):
        self._se = se
        self._artist_ranker = artist_ranker

    def get_se(self):
        return self._se

    def get_artist_ranker(self):
        return self._artist_ranker