import time
import signal
import typing
import logging

from . import leds

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class App():
    def __init__(self):
        log.info('Initializing...')
        log.info('Initialized.')

    def run(self):
        log.info('Running...')

        while True:
            self.loop()

    def loop(self):
        leds.RGBLeds().test()

        # leds.blinking_led_loop()
