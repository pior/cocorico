import logging
import os.path

from .amplifier import Amplifier
from .engine import Engine

log = logging.getLogger(__name__)


class Sound:
    ALARM_FILE = 'cuckoo.wav'
    STARTUP_FILE = 'hello-man.wav'

    def __init__(self):
        self._amplifier = Amplifier()
        self._engine = Engine()

        self._playing = None

    def close(self):
        self._amplifier.close()
        self._engine.close()

    def play_startup(self):
        self._start(self.STARTUP_FILE)

    def play_alarm(self):
        if self._playing == self.ALARM_FILE and self._engine.is_playing():
            return
        self._start(self.ALARM_FILE)

    def refresh(self):
        if not self._engine.is_playing():
            self.stop()

    def _start(self, name):
        log.info("Playing %s", name)

        self._amplifier.enable()

        path = os.path.join('sounds', name)
        self._engine.start(path)

        self._playing = name

    def stop(self):
        self._engine.stop()
        self._amplifier.disable()
        self._playing = None
