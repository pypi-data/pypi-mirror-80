from .SpAuth import SpAuth
from .objects.SpPlaylist import SpotifyPlaylist
from .objects.SpTrack import SpotifyTrack


class SpSearchPlaylist(SpAuth):
    def search(self, id):
        results = self.client.playlist(id)
        response = self.client.playlist_tracks(id)
        results['tracks']['items'] = list()

        while True:
            for ite, item in enumerate(response['items']):
                response['items'][ite] = SpotifyTrack(item['track']).to_dict()

            results['tracks']['items'].extend(response['items'])
            if response['next'] is None:
                break
            response = self.client.next(response)

        if len(results['tracks']['items']) != results['tracks']['total']:
            raise Exception('To Do')

        return SpotifyPlaylist(results)
