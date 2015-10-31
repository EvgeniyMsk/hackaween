import numpy as np

class EventRanker(object):

    def __init__(self, ranking_cfg):
        pass

    def rank(self, events, artists):
        features = {}

        for id, event in events.iteritems():
            features[id] = {"priority": 0}
            for artist in artists:
                if artist['artist'] in event['title']:
                    features[id]["priority"] = artist["count"]

        fields = features.values()
        priors = map(lambda x: x["priority"], fields)
        mean = np.mean(priors)
        std = np.std(priors)

        def cmp(x):
            return (features[x]["priority"] - mean) / std

        sorted_ids = sorted(events, key = cmp, reverse=True)
        res = []
        for id in sorted_ids:
            res.append(events[id])
        return res




