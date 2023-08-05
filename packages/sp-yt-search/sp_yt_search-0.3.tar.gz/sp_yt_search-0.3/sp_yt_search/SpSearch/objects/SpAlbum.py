from .Spotify import Spotify

OBJECT_TYPE = 'album'


class SpotifyAlbum(Spotify):
    def __init__(self, data):
        self.type = OBJECT_TYPE
        super(SpotifyAlbum, self).__init__(data)

    def parse_data(self, data):
        return data

    def tracks(self):
        return self.data['tracks']['items']

    def to_dict(self):
        return self.data
