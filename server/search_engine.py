# -*- coding: utf-8 -*-

from elasticsearch import client, Elasticsearch

class SearchEngine(object):

    def __init__(self):
        es = Elasticsearch()
        esClient = client.IndicesClient(es)
        # esClient.delete(index = '_all')
        # esClient.create(index = 'mytemp', body =  {
        #   "settings": {
        #     "analysis": {
        #         "tokenizer":{
        #       "nGram":{
        #         "type": "nGram",
        #         "min_gram": 4,
        #         "max_gram": 20
        #             }
        #         },
        #       "filter": {
        #         "stopwords_ru": {
        #         "type": "stop",
        #         "stopwords": ['а','без','более','бы','был','была','были','было','быть','в','вам','вас','весь','во','вот','все','всего','всех','вы','где','да','даже','для','до','его','ее','если','есть','еще','же','за','здесь','и','из','или','им','их','к','как','ко','когда','кто','ли','либо','мне','может','мы','на','надо','наш','не','него','нее','нет','ни','них','но','ну','о','об','однако','он','она','они','оно','от','очень','по','под','при','с','со','так','также','такой','там','те','тем','то','того','тоже','той','только','том','ты','у','уже','хотя','чего','чей','чем','что','чтобы','чье','чья','эта','эти','это','я'],
        #         "ignore_case": "true"
        #         },
        #       "custom_word_delimiter": {
        #         "type": "word_delimiter",
        #         # "PowerShot" ⇒ "Power" "Shot", части одного слова становятся отдельными токенами
        #         "generate_word_parts": "true",
        #         "generate_number_parts": "true",  # "500-42" ⇒ "500" "42"
        #         "catenate_words": "true",  # "wi-fi" ⇒ "wifi"
        #         "catenate_numbers": "false",  # "500-42" ⇒ "50042"
        #         "catenate_all": "true",  # "wi-fi-4000" ⇒ "wifi4000"
        #         "split_on_case_change": "true",  # "PowerShot" ⇒ "Power" "Shot"
        #         "preserve_original": "true",  # "500-42" ⇒ "500-42" "500" "42"
        #         "split_on_numerics": "false"  # "j2se" ⇒ "j" "2" "se"
        #       }
        # },
        #     "analyzer": {
        #         "russian": {
        #           "tokenizer":  "nGram",
        #           "filter": [
        #               "custom_word_delimiter",
        #               "stopwords_ru"
        #           ]
        #         }
        #     }
        #     }
        #   }
        # }
        # )
        self._es = es
        self._esc = esClient
        pass

    def load(self, events):
        for i in events['results']:
            d = {'title': i['title'], 'date': i['dates'][0]['start']}
            self._es.index(index='mytemp', doc_type='event', id=i['id'], body=d)

    def search(self, requests):
        sset = set()
        result = []
        for i in requests:
            res = self._es.search(index="mytemp", body={'fields': ['title', 'date'], 'query': {'match': {'title': '{}'.format(i['artist'])}}})
            for item in res['hits']['hits']:
                if not (item['_id'] in sset):
                    result.append({'title' : item['fields']['title'], 'date' : item['fields']['date']})
                    sset.add(item['_id'])
        return result