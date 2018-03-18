import time
import signal
import typing
import logging

from .light.leds import RGBLeds
from .display import Display
from .button import Button
from .clock import Clock

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class App():
    def __init__(self):
        log.info('Initializing...')
        self.clock = Clock()
        self.display = Display()
        # self.btn_alarm = Button(pin=17, callback=self.btn_alarm_cb)
        # self.btn_alarm_time = Button(pin=27, callback=self.btn_alarm_time_cb)
        log.info('Initialized.')

    def run(self):
        log.info('Running...')
        self.refresh_display()
        while True:
            self.loop()

    def loop(self):
            # RGBLeds().test()
            # leds.blinking_led_loop()
            self.refresh_display()
            time.sleep(1)

    # def btn_alarm_cb(self):
    #     self.counter += 1
    #     self.refresh_display()

    # def btn_alarm_time_cb(self):
    #     self.counter = max(0, self.counter - 1)
    #     self.refresh_display()

    def refresh_display(self):
        self.display.as_clock(self.clock.time_str)
