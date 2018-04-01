import threading
import time


class PeriodicTask(threading.Thread):
    def __init__(self, period, func):
        super().__init__()
        self._func = func
        self._period = period
        self._stopping = threading.Event()
        self.setDaemon(1)

    def run(self):
        while not self._stopping.is_set():
            self._func()
            self._stopping.wait(timeout=self._period)

    def stop(self):
        self._stopping.set()
