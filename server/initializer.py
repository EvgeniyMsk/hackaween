# -*- coding: utf-8 -*-

import context
import search_engine

class Initializer(object):

    @staticmethod
    def get_context():
        se = search_engine.SearchEngine()
        return context.Context(se)
