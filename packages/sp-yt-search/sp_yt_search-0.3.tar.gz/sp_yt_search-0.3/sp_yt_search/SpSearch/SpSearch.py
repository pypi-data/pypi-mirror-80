from .SpSearchAlbum import SpSearchAlbum
from .SpSearchArtist import SpSearchArtist
from .SpSearchPlaylist import SpSearchPlaylist
from .SpSearchTrack import SpSearchTrack

TRACK_STRATEGY_NAME = 'track'
PLAYLIST_STRATEGY_NAME = 'playlist'
ALBUM_STRATEGY_NAME = 'album'
ARTIST_STRATEGY_NAME = 'artist'


class SpSearch:
    def __init__(self, uri):
        self.strategy = list(uri.split(":"))[1]
        self.resource_id = list(uri.split(":"))[2]
        self.result = self.spotify().search(self.resource_id)

    def spotify(self):
        if self.strategy == TRACK_STRATEGY_NAME:
            return SpSearchTrack()
        if self.strategy == PLAYLIST_STRATEGY_NAME:
            return SpSearchPlaylist()
        if self.strategy == ALBUM_STRATEGY_NAME:
            return SpSearchAlbum()
        if self.strategy == ARTIST_STRATEGY_NAME:
            return SpSearchArtist()

    def to_dict(self):
        return self.result.to_dict()

    def tracks(self):
        return self.result.tracks()
