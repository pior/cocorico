import datetime
import logging
import signal
import sys
import time

from .app import App
from .clock import Clock

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    app = App()

    def terminate(signum, _):
        log.warning("Received signal %s", signum)
        app.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)

    run(app)


def run(app):
    clock = Clock()

    time_previous = clock.now

    app.initialize()

    while True:
        time_now = clock.now
        app.routine(time_previous, time_now)
        time_previous = time_now

        next_time = time_previous + datetime.timedelta(seconds=1)
        delta = next_time - clock.now
        time.sleep(delta.total_seconds())


if __name__ == '__main__':
    main()
