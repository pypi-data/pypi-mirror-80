from .SpAuth import SpAuth
from .objects.SpTrack import SpotifyTrack


class SpSearchTrack(SpAuth):
    def search(self, id):
        return SpotifyTrack(self.client.track(id))
