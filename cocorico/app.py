import time
import signal
import typing
import logging

import gpiozero

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class App():
    def __init__(self):
        self.led1 = gpiozero.LED(22)
        self.led2 = gpiozero.LED(23)
        log.info('Application initialized.')

    def run(self):
        log.info('Application running...')
        self.loop()

    def loop(self):
        state = False

        while True:
            state = not state
            self.led1.value = state
            self.led2.value = not state
            time.sleep(0.2)
