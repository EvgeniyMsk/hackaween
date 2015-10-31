# -*- coding: utf-8 -*-

from elasticsearch import client, Elasticsearch

class SearchEngine(object):

    def __init__(self):
        es = Elasticsearch([{'host': "10.25.3.181", 'port': 9200}])
        esClient = client.IndicesClient(es)
        self._es = es
        self._esc = esClient
        pass

    def load(self, events):
        for i in events['results']:
            d = {'title': i['title'], 'date': i['dates'][0]['start'], 'place': i['place']['address'], 'desc' : i['description'], 'img' : i['images'][0]['image']}
            self._es.index(index='mytemp', doc_type='event', id=i['id'], body=d)

    def search(self, requests):
        sset = set()
        result = []
        for artist in requests:
            res = self._es.search(index="stable",
                                  body={
                                      'fields': ['title', 'date', 'place', 'img', 'desc'],
                                      'query': {'match': {'title': '{}'.format(artist)}}
                                  })

            for item in res['hits']['hits']:
                if not (item['_id'] in sset):
                    result.append({
                        'title' : item['fields']['title'][0],
                        'place': item['fields']['place'][0],
                        'date' : item['fields']['date'][0],
                        'desc' : item['fields']['desc'][0],
                        'img' : item['fields']['img'][0]
                    })
                    sset.add(item['_id'])

        return result

    def create_index(self, name):
            if not self._esc.exists(index = name):
                self._esc.create('mytemp')
                entry_mapping = {
                    'event': {
                        'properties': {
                                'date': {'type': 'integer'},
                                'title': {'type': 'string', "tokenizer" : 'keyword', 'analyzer':"russian"},
                                'place' : {'type':'string'},
                                'img' : {'type' : 'string'},
                                'desc' : {'type' : 'string'}
                                        }
                                }
                            }
                self._esc.put_mapping(index = 'mytemp', doc_type='event', body = entry_mapping)

    def delete_indexes(self):
        self._esc.delete(index = '_all')
