# -*- coding: utf-8 -*-

import context

from search_engine import SearchEngine
from artist_ranker import ArtistRanker

class Initializer(object):

    @staticmethod
    def get_context():
        se = SearchEngine()
        artist_ranker = ArtistRanker()
        return context.Context(se=se, artist_ranker=artist_ranker)
