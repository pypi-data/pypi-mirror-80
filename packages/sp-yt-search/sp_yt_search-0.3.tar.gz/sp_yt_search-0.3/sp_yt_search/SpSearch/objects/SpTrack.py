from .Spotify import Spotify

OBJECT_TYPE = 'track'


class SpotifyTrack(Spotify):
    def __init__(self, data):
        self.type = OBJECT_TYPE
        super(SpotifyTrack, self).__init__(data)

    def parse_data(self, data):
        if 'available_markets' in data:
            del data['available_markets']
        if 'is_local' in data:
            del data['is_local']
        if 'album' in data:
            if 'available_markets' in data['album']:
                del data['album']['available_markets']
        data['c'] = dict();
        data['c']['duration'] = int(data['duration_ms'] / 1000)
        data['c']['full_name'] = ', '.join(
            [str(elem['name']) for elem in data['artists']]) + f" - {data['name']}"
        data['c']['is_remix'] = 'remix' in data['name'].lower()
        data['c']['is_instrumental'] = 'instrumental' in data['name'].lower()
        data['c']['is_live'] = 'live' in data['name'].lower()
        data['c']['is_official'] = not data['c']['is_remix'] and not data['c']['is_instrumental']
        return data

    def tracks(self):
        result = list()
        result.append(self.data);
        return result

    def to_dict(self):
        return self.data
