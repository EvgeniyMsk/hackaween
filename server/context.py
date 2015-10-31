# -*- coding: utf-8 -*-

class Context(object):

    def __init__(self, se, artist_ranker, http_cfg, kudago_cfg, es_cfg):
        self._se = se
        self._artist_ranker = artist_ranker
        self._http_cfg = http_cfg
        self._kudago_cfg = kudago_cfg
        self._es_cfg = es_cfg

    def get_se(self):
        return self._se

    def get_artist_ranker(self):
        return self._artist_ranker

    def get_http_cfg(self):
        return self._http_cfg

    def get_kudago_cfg(self):
        return self._kudago_cfg

    def get_es_cfg(self):
        return self._es_cfg