from .SpAuth import SpAuth
from .objects.SpAlbum import SpotifyAlbum
from .objects.SpTrack import SpotifyTrack


class SpSearchAlbum(SpAuth):
    def search(self, id):
        results = self.client.album(id)
        response = self.client.album_tracks(id)
        results['tracks']['items'] = list()

        while True:
            for ite, item in enumerate(response['items']):
                response['items'][ite] = SpotifyTrack(item).to_dict()

            results['tracks']['items'].extend(response['items'])
            if response['next'] is None:
                break
            response = self.client.next(response)

        if len(results['tracks']['items']) != results['total_tracks']:
            raise Exception('To Do')

        return SpotifyAlbum(results)
