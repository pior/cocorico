import time
import signal
import typing
import logging

from .light.leds import RGBLeds
from . import display

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
        # RGBLeds().test()
        # leds.blinking_led_loop()

        text = str(int(time.time() % 10000))
        display.test(text)
        time.sleep(1)
