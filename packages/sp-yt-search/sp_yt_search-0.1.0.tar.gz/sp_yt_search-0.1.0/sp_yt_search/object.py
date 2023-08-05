from difflib import SequenceMatcher

from .helpers import GetNumbersFromString, DateTimeStringToSeconds
from .settings import BONUS_RATES, YT_BASE_URL, FILE_DIR, FILE_EXT

TITLE = {
    'OFFICIALS': ['(Official Video)', '(Official Music Video)'],
    'DUMP_STAMPS': ['Official Video', 'Official Music Video', 'HQ', 'HD'],
}
CHANNEL = {
    'OFFICIALS': ['Official']
}
EMPTY_BRACKETS = ['()', '( )', '[]', '[ ]', '{}', '{ }']


class YouTube():
    def __init__(self, spotify_track, video_data):
        self.SPOTIFY_TRACK = spotify_track
        self.data = self.parseVideoData(video_data)

    def parseVideoData(self, video_data):
        res = dict()
        res['id'] = video_data.get('videoId', None)
        res['channel'] = video_data.get('longBylineText', {}).get('runs', [[{}]])[0].get('text', None)
        res['url_suffix'] = video_data.get('navigationEndpoint', {}).get('commandMetadata', {}).get(
            'webCommandMetadata', {}).get('url', None)
        res['title'] = video_data.get('title', {}).get('runs', [[{}]])[0].get('text', None)
        res['url'] = self.parseURL(
            video_data.get('navigationEndpoint', {}).get('commandMetadata', {}).get('webCommandMetadata', {}).get('url',
                                                                                                                  None))
        res['duration'] = self.parseDuration(video_data.get('lengthText', {}).get('simpleText', 0))
        res['views'] = self.parseViews(video_data.get('viewCountText', {}).get('simpleText', 0))
        res['search_ratio'] = self.countSearchRatio(res)
        res['save_path'] = self.parsePath(self.SPOTIFY_TRACK['c']['full_name'])
        return res

    def parsePath(self, full_name):
        prefix = FILE_DIR[:-1] if FILE_DIR.endswith('/') else FILE_DIR
        ext = FILE_EXT[1:] if FILE_EXT.startswith('.') else FILE_EXT

        # remove dump stamps
        for dump_stamp in TITLE['DUMP_STAMPS']:
            full_name.replace(dump_stamp, '')
        # removes multiple spaces
        full_name = ' '.join(full_name.split()).replace('/', '_')
        # returns value without leading and trailing space and mp3 extension

        return f'{prefix}/{full_name.strip()}.{ext}'

    def parseURL(self, url):
        return f'{YT_BASE_URL}{url}'

    def parseDuration(self, duration):
        return DateTimeStringToSeconds(duration)

    def parseViews(self, views):
        return GetNumbersFromString(views)

    def parseFilename(self, title):
        # remove dump stamps
        for dump_stamp in TITLE['DUMP_STAMPS']:
            title = title.replace(dump_stamp, '')
        # removes multiple spaces
        title = ' '.join(title.split())
        # returns value without leading and trailing space and mp3 extension
        for dump_stamp in EMPTY_BRACKETS:
            title = title.replace(dump_stamp, '')

        return title.strip()

    def countSearchRatio(self, res):
        search_ratio = dict()

        search_ratio['title'] = self.rateTitle(res['title'].lower())
        if search_ratio['title'] >= 0.6:
            search_ratio['channel'] = self.rateChannel(res['channel'].lower())
        search_ratio['duration'] = self.rateDuration(res['duration'])

        search_ratio['whole'] = sum(search_ratio.values())
        return search_ratio

    def rateTitle(self, title_lowercase):
        rate = round(SequenceMatcher(None, title_lowercase, self.SPOTIFY_TRACK['c']['full_name'].lower()).ratio(), 2)
        if self.SPOTIFY_TRACK['c']['is_official'] and any(
                official in title_lowercase for official in TITLE['OFFICIALS']):
            rate += BONUS_RATES['OFFICIAL']
        if self.SPOTIFY_TRACK['c']['is_remix'] and 'remix' in title_lowercase:
            rate += BONUS_RATES['REMIX']
        if self.SPOTIFY_TRACK['c']['is_instrumental'] and 'instrumental' in title_lowercase:
            rate += BONUS_RATES['INSTRUMENTAL']
        if self.SPOTIFY_TRACK['c']['is_live'] and 'live' in title_lowercase:
            rate += BONUS_RATES['LIVE']
        return rate

    def rateChannel(self, channel_lowercase):
        rate = round(SequenceMatcher(None, channel_lowercase, self.SPOTIFY_TRACK['c']['full_name'].lower()).ratio(), 2)
        if any(official in channel_lowercase for official in CHANNEL['OFFICIALS']):
            rate += BONUS_RATES['CHANNEL']
        return rate

    def rateDuration(self, duration):
        return (1 - (abs(duration - self.SPOTIFY_TRACK['c']['duration']) / 100))

    def to_dict(self):
        return self.data
