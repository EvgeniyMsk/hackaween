import operator


class ArtistRanker(object):

    def __init__(self, ranking_cfg):
        self._min_count = ranking_cfg["min_artist_count"]

    def rank(self, music, top_count):
        return self._get_top_artists(music, top_count)

    def _get_top_artists(self, artists, top_count):
        artists = map(lambda x: x["artist"], artists)
        uniq_artists = {}
        for artist in artists:
            if artist in uniq_artists:
                uniq_artists[artist] += 1
            else:
                uniq_artists[artist] = 1

        sorted_artists = sorted(uniq_artists.items(), key=operator.itemgetter(1), reverse=True)
        top = filter(lambda x: x[1] >= self._min_count, sorted_artists) #sorted_artists[:top_count]
        res = []
        for artist, count in top:
            res.append({"artist":artist, "count":count})
        return res


if __name__ == "__main__":

    import json

    fd = open('music.json')
    music = json.load(fd)['music']

    ranker = ArtistRanker()
    top = ranker.rank(music, 10)
    print top