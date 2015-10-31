


class ArtistRanker(object):

    def __init__(self):
        pass

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

        sorted_artists = sorted(uniq_artists, key=uniq_artists.get, reverse=True)
        top = sorted_artists[:top_count]
        res = []
        for artist in top:
            res.append({"artist":artist, "count":uniq_artists[artist]})
        return res


if __name__ == "__main__":

    import json

    fd = open('music.json')
    music = json.load(fd)['music']

    ranker = ArtistRanker()
    top = ranker.rank(music, 10)
    print top