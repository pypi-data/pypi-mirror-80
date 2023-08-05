from ..Singleton import Singleton


class SpSettings(metaclass=Singleton):
    def __init__(self):
        self.SPOTIPY_CLIENT_ID = None
        self.SPOTIPY_CLIENT_SECRET = None
