from .Spotify import Spotify

OBJECT_TYPE = 'playlist'


class SpotifyPlaylist(Spotify):
    def __init__(self, data):
        self.type = OBJECT_TYPE
        super(SpotifyPlaylist, self).__init__(data)

    def parse_data(self, data):
        del data['primary_color']
        del data['public']
        del data['followers']
        return data

    def tracks(self):
        return self.data['tracks']['items']

    def to_dict(self):
        return self.data
