import logging
import subprocess

import simpleaudio

log = logging.getLogger(__name__)


def tweak_alsa():
    cmd = 'amixer set Master 100% unmute'

    log.info("Trying to configure the alsa mixer: %s", cmd)
    try:
        subprocess.run(cmd.split())
    except Exception as exc:
        log.error("Failed: %s", exc)


class AlsaPlayer:
    def __init__(self):
        self._play_obj = None
        tweak_alsa()

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
