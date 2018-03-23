import wave
from threading import Thread, Event

from queue import Queue, Empty
import logging

log = logging.getLogger(__name__)


class Worker(Thread):

    def __init__(self, player):
        Thread.__init__(self)
        self.setDaemon(True)

        self.queue = Queue()
        self.stop_requested = Event()

        self.player = player

    def play_once(self, path):
        log.info("Play once %s", path)
        self.queue.put(path)

    def play_loop(self, path):
        log.info("Play loop %s", path)

    def stop(self):
        try:
            while True:
                self.queue.get_nowait()
        except Empty:
            pass

        self.stop_requested.set()
        self.player.stop()

    def run(self):
        log.info("Sound worker started")

        while True:
            path = self.queue.get()
            log.info("Start playing %s", path)

            self.player.start(path)

            log.info("Completed %s", path)
            self.queue.task_done()
