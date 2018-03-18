import time
import signal
import typing
import logging

from .light.leds import RGBLeds
from .display import Display
from .button import Button

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class App():
    def __init__(self):
        log.info('Initializing...')
        self.display = Display()
        self.button = Button(pin=17, callback=self.btn_callback)
        self.counter = 0
        log.info('Initialized.')

    def run(self):
        log.info('Running...')
        while True:
            self.loop()

    def loop(self):
            # RGBLeds().test()
            # leds.blinking_led_loop()

            text = str(int(self.counter))
            self.display.announce(text)

            self.counter += 1
            time.sleep(1)

    def btn_callback(self):
        self.counter = 0
