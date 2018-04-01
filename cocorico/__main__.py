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

        td = clock.now + datetime.timedelta(seconds=1) - time_previous
        time.sleep(td.total_seconds())


main()
