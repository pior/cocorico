import threading
import time


class PeriodicTask(threading.Thread):
    def __init__(self, period, func):
        super().__init__()
        self._func = func
        self._period = period
        self.setDaemon(1)

    def run(self):
        while self._func:
            self._func()
            time.sleep(self._period)
