import json
import urllib.parse

import requests

from .object import YouTube
from .settings import YT_MAX_RESULTS, YT_BASE_URL


class Search:
    def __init__(self, track, max_results=YT_MAX_RESULTS):
        self.TRACK = track
        self.MAX_RESULTS = max_results
        self.VIDEOS = self.search()

    def search(self):
        encoded_search = urllib.parse.quote(self.TRACK['c']['full_name'])
        url = f'{YT_BASE_URL}/results?search_query={encoded_search}'
        response = requests.get(url).text
        while 'window["ytInitialData"]' not in response:
            response = requests.get(url).text
        results = self.parse_html(response)
        if self.MAX_RESULTS is not None and len(results) > self.MAX_RESULTS:
            return results[: self.MAX_RESULTS]
        return results

    def parse_html(self, response):
        results = list()
        start = (
                response.index('window["ytInitialData"]')
                + len('window["ytInitialData"]')
                + 3
        )
        end = response.index('};', start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = \
            data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0][
                'itemSectionRenderer']['contents']

        for video in videos:
            if 'videoRenderer' in video.keys():
                video_data = video.get('videoRenderer', {})
                results.append(YouTube(self.TRACK, video_data).to_dict())

        results.sort(key=lambda res: res['search_ratio']['whole'], reverse=True)
        return results

    def getBestMatch(self):
        return self.VIDEOS[0]

    def to_dict(self):
        return self.VIDEOS

    def to_json(self):
        return json.dumps({'videos': self.VIDEOS})
