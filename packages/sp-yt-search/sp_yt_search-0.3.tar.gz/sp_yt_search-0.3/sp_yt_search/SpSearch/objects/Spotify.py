import abc


class Spotify:
    def __init__(self, data):
        if data['type'] != self.type:
            raise Exception('To Do')

        self.data = self.parse_data(data)

    @abc.abstractmethod
    def parse_data(self):
        pass

    @abc.abstractmethod
    def to_dict(self):
        pass
