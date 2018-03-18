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
        self.button1 = Button(pin=17, callback=self.btn1_callback)
        self.button2 = Button(pin=27, callback=self.btn2_callback)
        self.counter = 0
        log.info('Initialized.')

    def run(self):
        log.info('Running...')
        self.refresh_display()
        while True:
            self.loop()

    def loop(self):
            # RGBLeds().test()
            # leds.blinking_led_loop()
            time.sleep(1)

    def btn1_callback(self):
        self.counter += 1
        self.refresh_display()

    def btn2_callback(self):
        self.counter = max(0, self.counter - 1)
        self.refresh_display()

    def refresh_display(self):
        even = self.counter % 2 == 0
        text = "%s  %s" % ('EVEN' if even else 'ODD ', self.counter)
        self.display.announce(text)
