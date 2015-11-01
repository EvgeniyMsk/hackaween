# -*- coding: utf-8 -*-

import os
import json

import context

from search_engine import SearchEngine
from artist_ranker import ArtistRanker
from event_ranking import EventRanker

class Initializer(object):

    @staticmethod
    def get_context():

        srv_cfg = Initializer._read_cfg("server")
        http_cfg = srv_cfg["http"]
        kudago_cfg = srv_cfg["kudago"]
        ranking_cfg = srv_cfg["ranking"]
        es_cfg = Initializer._read_cfg("elasticsearch")

        se = SearchEngine(es_cfg)
        artist_ranker = ArtistRanker(ranking_cfg)
        event_ranker = EventRanker(ranking_cfg)
        return context.Context(se=se,
                               artist_ranker=artist_ranker,
                               event_ranker=event_ranker,
                               http_cfg=http_cfg,
                               kudago_cfg=kudago_cfg,
                               es_cfg=es_cfg)


    @staticmethod
    def _read_cfg(cfg_name):
        cfg_dir = os.path.dirname(os.path.realpath(__file__))
        cfg_dir = os.path.join(cfg_dir, "config")
        cfg_ext = ".cfg"
        cfg_file = os.path.join(cfg_dir, cfg_name + cfg_ext)
        with open(cfg_file) as fd:
            tmp = fd.read().decode("utf-8")
            return json.loads(tmp)