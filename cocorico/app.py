import time
import signal
import typing
import logging

from .light.leds import RGBLeds
from .display import Display

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class App():
    def __init__(self):
        pass

    def run(self):
        log.info('Initializing...')
        display = Display()

        log.info('Initialized.')

        log.info('Running...')
        while True:
            # RGBLeds().test()
            # leds.blinking_led_loop()

            text = str(int(time.time() % 10000))
            display.announce(text)

            time.sleep(1)
