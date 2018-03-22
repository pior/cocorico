import wave
from threading import Thread
from queue import Queue
import logging

log = logging.getLogger(__name__)


class Worker(Thread):

    def __init__(self, player):
        Thread.__init__(self)
        self.setDaemon(True)
        self.queue = Queue()
        self.player = player

    def enqueue(self, path):
        log.info("Enqueued %s", path)
        self.queue.put(path)

    def run(self):
        log.info("Sound worker started")

        while True:
            path = self.queue.get()
            log.info("Start playing %s", path)

            self.player.start(path)

            log.info("Completed %s", path)
            self.queue.task_done()
