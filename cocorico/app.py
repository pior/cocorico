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
        self.loop()

    def loop(self):
        leds.RGBLeds().test(speed=16_000_000)
        leds.RGBLeds().test(speed=4_000_000)
        leds.RGBLeds().test(speed=1_000_000)
        leds.RGBLeds().test(speed=400_000)

        leds.blinking_led_loop()
