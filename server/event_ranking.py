import numpy as np

class EventRanker(object):

    def __init__(self, ranking_cfg):
        self._events_count = ranking_cfg["events_count"]
        self._alpha = ranking_cfg["artist_count_coef"]
        self._beta = ranking_cfg["favorites_coef"]
        self._gamma = ranking_cfg["comments_coef"]
        pass

    def rank(self, events, artists):
        features = {}

        for id, event in events.iteritems():
            features[id] = {"priority": 0, "com_count" : event['com_count'], "fav_count" : event['fav_count']}
            for artist in artists:
                if artist['artist'] in event['title']:
                    features[id]["priority"] = artist["count"]

        fields = features.values()
        stat = {}
        stat["priority"]  = self._get_stat("priority", fields)
        stat["com_count"] = self._get_stat("com_count", fields)
        stat["fav_count"] = self._get_stat("fav_count", fields)

        def cmp(x):
            prior = (features[x]["priority"] - stat["priority"][0]) / stat["priority"][1]
            fav = (features[x]["fav_count"] - stat["fav_count"][0]) / stat["fav_count"][1]
            com = (features[x]["com_count"] - stat["com_count"][0]) / stat["com_count"][1]
            return self._alpha * prior + self._beta * fav + self._gamma * com

        sorted_ids = sorted(events, key = cmp, reverse=True)
        res = []
        for id in sorted_ids:
            res.append(events[id])
        return res[:self._events_count]

    def _get_stat(self, field, fields):
        priors = map(lambda x: x[field], fields)
        return (np.mean(priors), np.std(priors))



