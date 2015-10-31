# -*- coding: utf-8 -*-

class EventAdviser(object):

    def __init__(self, se):
        self._se = se
        pass

    def search(self, requests):
        return self._se.search(requests)
