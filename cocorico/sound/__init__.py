import os.path

from .amplifier import Amplifier
# from .worker import Worker
from . import engine


class Sound:
    ALARM_FILE = 'cuckoo.wav'
    STARTUP_FILE = 'hello-man.wav'

    def __init__(self):
        self._amplifier = Amplifier()
        self._engine = engine.build()

        self._playing = None

    def for_startup(self):
        self._start(self.STARTUP_FILE)

    def for_alarm(self):
        if self._playing == self.ALARM_FILE and self._engine.is_playing():
            return
        self._start(self.ALARM_FILE)

    def standby(self):
        if self._playing:
            self._playing = None
        self._engine.stop()
        self._amplifier.disable()

    def _start(self, name):
        self._amplifier.enable()

        if self._engine.is_playing:
            self._engine.stop()

        path = os.path.join('sounds', name)
        self._engine.start(path)

        self._playing = name
