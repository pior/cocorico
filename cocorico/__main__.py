import atexit
import datetime
import time
import logging

from .app import App
from .clock import Clock

logging.basicConfig(level=logging.INFO)


def main():
    app = App()
    atexit.register(app.close)

    clock = Clock()

    time_previous = None
    while True:
        time_now = clock.now
        app.routine(time_previous, time_now)

        time_previous = time_now

        time.sleep(1)  # There MUST be a better way 😏

main()
