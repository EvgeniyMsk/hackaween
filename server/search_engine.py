# -*- coding: utf-8 -*-

import logging

from elasticsearch import client, Elasticsearch

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

            data = {'title': title,
                    'date': date,
                    'place': place,
                    'desc' : desc,
                    'img' : img}
            #logging.debug("Load to index event {}".format(title.decode("utf-8", "ignore").encode("utf-8")))
            self._es.index(index=self._index, doc_type='event', id=event['id'], body=data)

    def search(self, requests):
        sset = set()
        result = []
        for artist in requests:

            try:
                res = self._es.search(index=self._index,
                                      body={
                                          'fields': ['title', 'date', 'place', 'img', 'desc'],
                                          'query': {'match': {'title': '{}'.format(artist)}}
                                      })

                for item in res['hits']['hits']:
                    if not (item['_id'] in sset):
                        result.append({
                            'title': item['fields']['title'][0],
                            'place': item['fields']['place'][0],
                            'date': item['fields']['date'][0],
                            'desc': item['fields']['desc'][0],
                            'img': item['fields']['img'][0]
                        })
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

