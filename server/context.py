# -*- coding: utf-8 -*-

class Context(object):

    def __init__(self, se):
        self._se = se

    def get_se(self):
        return self._se