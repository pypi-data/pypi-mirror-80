from ..Singleton import Singleton


class YtSettings(metaclass=Singleton):
    def __init__(self):
        self.YT_MAX_RESULTS = 5
        self.YT_BASE_URL = 'https://youtube.com'

        self.FILE_DIR = 'download'
        self.FILE_EXT = 'mp3'

        self.BONUS_RATES = {
            'OFFICIAL': .5,
            'REMIX': .5,
            'INSTRUMENTAL': .5,
            'LIVE': .5,
            'CHANNEL': .3
        }
