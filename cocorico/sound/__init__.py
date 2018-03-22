import os.path

from cocorico.hal.gpio import GPIO
from .worker import Worker


def build_player():
    try:
        from .alsa import AlsaPlayer as Player
    except ImportError:
        from .afplay import Afplay as Player

    player = Player()
    return Worker(player)


class Sound:
    # SHUTDOWN_PIN = 4  # BCM pin 4

    def __init__(self):
        # GPIO.setup(self.SHUTDOWN_PIN, GPIO.OUT, initial=GPIO.LOW)

        self.worker = build_player()
        self.worker.start()

        # self._shutdown = False

    # def close(self):
    #     GPIO.cleanup(self.SHUTDOWN_PIN)
    #     pygame.mixer.quit()

    # def _enable(self):
    #     if self._shutdown:
    #         GPIO.output(self.SHUTDOWN_PIN, GPIO.HIGH)
    #         self._shutdown = False

    # def _disable(self):
    #     if not self._shutdown:
    #         GPIO.output(self.SHUTDOWN_PIN, GPIO.LOW)
    #         self._shutdown = True

    def start(self, filename):
        # self._enable()
        path = os.path.join('sounds', filename)
        self.worker.enqueue(path)


    # def shutdown_if_possible(self):
    #     if not self.playing:
    #         self._disable()

    # @property
    # def playing(self):
    #     return bool(pygame.mixer.music.get_busy())
