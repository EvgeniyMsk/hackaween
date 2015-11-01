# -*- coding: utf-8 -*-

import logging

from elasticsearch import client, Elasticsearch
import time

class SearchEngine(object):

    def __init__(self, cfg):
        es = Elasticsearch([{'host': cfg["host"], 'port': cfg["port"]}])
        esClient = client.IndicesClient(es)
        self._es = es
        self._esc = esClient
        self._index = cfg["index"]
        pass

    def load(self, events):
        for event in events['results']:

            title = self._get_title(event)
            date = self._get_date(event)
            place = self._get_place(event)
            desc = self._get_description(event)
            img = self._get_image(event)
            url = self._get_url(event)
            fav_count = self._get_fav_count(event)
            com_count = self._get_com_count(event)

            data = {'title': title,
                    'date': date,
                    'place': place,
                    'desc' : desc,
                    'img' : img,
                    'url' : url,
                    'fav_count' : fav_count,
                    'com_count' : com_count}
            #logging.debug("Load to index event {}".format(title.decode("utf-8", "ignore").encode("utf-8")))
            self._es.index(index=self._index, doc_type='event', id=event['id'], body=data)

    def search(self, requests):
        sset = set()
        result = {}
        for item in requests:

            try:
                # temp = ' AND '.join(item['artist'].split())
                res = self._es.search(index=self._index,
                                      body={
                                          'fields': ['title', 'date', 'place', 'img', 'desc', 'url', 'fav_count', 'com_count'],
                                          'query': {'match_phrase': {'title': '{}'.format(item['artist'])}}
                                      })

                for item in res['hits']['hits']:
                    if not (item['_id'] in sset):
                        temp =  item['fields']['desc'][0]
                        result[item['_id']] = {
                                'title': item['fields']['title'][0],
                                'place': item['fields']['place'][0],
                                'date': time.ctime(item['fields']['date'][0]),
                                'desc': item['fields']['desc'][0][3: len(temp) - 6],
                                'img': item['fields']['img'][0],
                                'url': item['fields']['url'][0],
                                'fav_count' :item['fields']['fav_count'][0],
                                'com_count' :item['fields']['com_count'][0]
                            }
                        sset.add(item['_id'])
            except Exception as exc:
                logging.error("Error while searching:{}".format(str(exc)))
        return result

    @staticmethod
    def _get_title(event):
        try:
            return event['title']
        except Exception as exc:
            logging.warning(str(exc))
            return "No title"

    @staticmethod
    def _get_fav_count(event):
        try:
            return event['favorites_count']
        except Exception as exc:
            logging.warning(str(exc))
            return "No fav_count"

    @staticmethod
    def _get_com_count(event):
        try:
            return event['comments_count']
        except Exception as exc:
            logging.warning(str(exc))
            return "No com_count"

    @staticmethod
    def _get_date(event):
        try:
            return event['dates'][0]['start']
        except Exception as exc:
            logging.warning(str(exc))
            return "No date"

    @staticmethod
    def _get_place(event):
        try:
            return event['place']['address']
        except Exception as exc:
            logging.warning(str(exc))
            return "No place"

    @staticmethod
    def _get_description(event):
        try:
            return event['description']
        except Exception as exc:
            logging.warning(str(exc))
            return "No description"
    @staticmethod
    def _get_url(event):
        try:
            return event['site_url']
        except Exception as exc:
            logging.warning(str(exc))
            return "No description"

    @staticmethod
    def _get_image(event):
        try:
            return event['images'][0]['image']
        except Exception as exc:
            logging.warning(str(exc))
            return "No image"

    def create_index(self, cfg):
        name = cfg["index"]
        if not self._esc.exists(index = name):
            self._esc.create(index = name)
            self._esc.put_mapping(index = name, doc_type='event', body = cfg["index_settings"])

    def delete_index(self, index):
        self._esc.delete(index=index)

