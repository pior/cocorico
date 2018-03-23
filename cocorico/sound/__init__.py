import os.path

from .amplifier import Amplifier
from .worker import Worker
from . import engine


class Sound:
    def __init__(self):
        self.amplifier = Amplifier()

        self.worker = Worker(engine.build())
        self.worker.start()

        self.in_alarm = False

    def for_startup(self):
        self._start('hello-man.wav')

    def for_alarm(self):
        self.in_alarm = True
        filename = 'cuckoo.wav'
        if self.playing != filename:
            self.playing = filename
            self._start(filename)

    def _start(self, name):
        self.amplifier.enable()
        path = os.path.join('sounds', name)
        self.worker.enqueue(path)

    def standby(self):
        self.worker.stop()
        self.in_alarm = False
        self.amplifier.disable()
