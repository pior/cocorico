import time


class Message:
    def __init__(self, persistence_time=3):
        self._persistence_time = persistence_time
        self._text = None
        self._until = 0

    def set(self, text):
        self._text = text
        self._until = time.time() + self._persistence_time

    def get(self):
        if time.time() > self._until:
            self._text = None
        return self._text
