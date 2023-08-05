import json

from .SpAuth import SpAuth


class SpSearchArtist(SpAuth):
    def search(self, id):
        results = self.client.artist(id)
        response = self.client.artist_albums(id)
        results['albums'] = list()

        with open('manual/data.json', 'w') as outfile:
            json.dump(response, outfile, indent=4, sort_keys=True)

        # while True:
        #     for item in response['items']:
        #         item['tracks'] = SpSearchAlbum().search(item['id'])
        #
        #     results['albums'].extend(response['items'])
        #
        #     if response['next'] is None:
        #         break
        #     response = self.client.next(response)
        #
        # if (len(results['albums']) != response['total']):
        #     raise Exception('To Do')
        #
        # return results
