import os.path

from .amplifier import Amplifier
from .worker import Worker
from . import engine


class Sound:
    def __init__(self):
        self.amplifier = Amplifier()

        self.worker = Worker(engine.build())
        self.worker.start()

        self.playing = None

    def for_startup(self):
        self._play('hello-man.wav')

    def for_alarm(self):
        filename = 'cuckoo.wav'
        if self.playing != filename:
            self.playing = filename
            self._play(filename)

    def _play(self, name):
        self.amplifier.enable()
        path = os.path.join('sounds', name)
        self.worker.enqueue(path)

    def silence(self):
        self.worker.stop()
        self.playing = None
        self.amplifier.disable()
