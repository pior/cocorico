import time
import signal
import typing
import logging

from .light.leds import RGBLeds
from .display import Display
from .button import Button
from .clock import Alarm, AlarmTimeSetting, Clock

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class App():
    def __init__(self):
        log.info('Initializing...')
        self.display = Display()
        self.clock = Clock()
        self.alarm_settings = AlarmTimeSetting()
        self.alarm = Alarm(clock=self.clock, settings=self.alarm_settings)

        self.btn_alarm_up = Button(pin=17, callback=self.btn_alarm_up_cb)
        self.btn_alarm_down = Button(pin=27, callback=self.btn_alarm_down_cb)
        log.info('Initialized.')

    def run(self):
        log.info('Running...')

        while True:
            self.periodic_routine()
            time.sleep(1)

    def periodic_routine(self):
        self.display.as_clock(self.clock.time)

    def btn_alarm_up_cb(self):
        self.alarm_settings.up()
        self.alarm_settings.set()
        self.display.as_set_alarm(self.alarm_settings.time)

    def btn_alarm_down_cb(self):
        self.alarm_settings.down()
        self.alarm_settings.set()
        self.display.as_set_alarm(self.alarm_settings.time)
