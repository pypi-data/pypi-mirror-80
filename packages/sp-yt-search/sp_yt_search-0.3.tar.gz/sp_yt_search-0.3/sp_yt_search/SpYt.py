from .SpSearch.SpSearch import SpSearch
from .SpSearch.SpSettings import SpSettings
from .YtSearch.YtSearch import YtSearch


class SpYt:
    def __init__(self, sp_client_id, sp_client_secret):
        self.data = None
        SpSettings().SPOTIPY_CLIENT_ID = sp_client_id
        SpSettings().SPOTIPY_CLIENT_SECRET = sp_client_secret
        pass

    def search(self, uri):
        data = SpSearch(uri)

        for track in data.tracks():
            track['c']['yt'] = YtSearch(track).to_dict()

        self.data = data
        return self.data
