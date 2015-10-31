__author__ = 'surok'

import search_engine

class Initializer(object):

    def __init__(self):
        self._se = search_engine.SearchEngine()
        self._se.create_index('mytemp')

    def getSE(self):
        return self._se