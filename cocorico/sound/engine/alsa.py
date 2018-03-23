import logging

import simpleaudio

log = logging.getLogger(__name__)


class AlsaPlayer:
    def __init__(self):
        self._play_obj = None

    def start(self, path):
        wave_object = simpleaudio.WaveObject.from_wave_file(path)
        log.info("Wave object from %s: %s", path, wave_object)

        self._play_obj = wave_object.play()
        log.info("Play object: %s", self._play_obj)

    def stop(self):
        if self._play_obj:
            log.info("Stop: %s", self._play_obj)
            self._play_obj.stop()
        self._play_obj = None

    def is_playing(self):
        if self._play_obj:
            return self._play_obj.is_playing()
        return False
