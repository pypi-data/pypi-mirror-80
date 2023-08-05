import json
import urllib.parse

import requests

from .objects.Yt import YouTube
from sp_yt_search.YtSearch.YtSettings import YtSettings


class YtSearch:
    def __init__(self, track):
        self.TRACK = track
        self.VIDEOS = self.do_search()

    def do_search(self):
        encoded_search = urllib.parse.quote(self.TRACK['c']['full_name'])
        url = f'{YtSettings().YT_BASE_URL}/results?search_query={encoded_search}'
        response = requests.get(url).text
        while 'window["ytInitialData"]' not in response:
            response = requests.get(url).text
        results = self.parse_html(response)
        if YtSettings().YT_MAX_RESULTS is not None and len(results) > YtSettings().YT_MAX_RESULTS:
            return results[: YtSettings().YT_MAX_RESULTS]
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

    def get_best_match(self):
        return self.VIDEOS[0]

    def to_dict(self):
        return self.VIDEOS

    def to_json(self):
        return json.dumps({'videos': self.VIDEOS})
