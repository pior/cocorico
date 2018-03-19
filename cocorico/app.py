import time
import logging

from .light.leds import RGBLeds
from .display import Display
from .display.state import State
from .button import Button
from .clock import Alarm, AlarmSettings, Clock

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)



class App():
    def __init__(self):
        log.info('Initializing...')
        self.display = Display()
        self.state = State()
        self.clock = Clock()
        self.alarm_settings = AlarmSettings()
        self.alarm = Alarm(clock=self.clock, settings=self.alarm_settings)

        self.btn_up = Button(pin=17, callback=self.btn_up_cb)
        self.btn_down = Button(pin=27, callback=self.btn_down_cb)
        self.btn_onoff = Button(pin=22, callback=self.btn_onoff_cb)
        self.btn_snooze = Button(pin=23, callback=self.btn_snooze_cb)
        log.info('Initialized.')

    def run(self):
        log.info('Running...')

        while True:
            self.periodic_routine()
            time.sleep(1)

    def periodic_routine(self):
        if self.alarm.triggered:
            log.info('Triggered!')
            self.state.set_alarm()
        self.refresh_display()

    def refresh_display(self):
        state = self.state.get()
        log.info("UI state = %s", state)

        if state == State.CLOCK:
            if self.alarm_settings.active:
                alarm_time = self.alarm_settings.time.strftime("%H:%M")
                text = alarm_time
            else:
                text = ''
            self.display.as_clock(self.clock.time, text)

        elif state == State.ALARM:
            self.display.as_clock(self.clock.time, "ALARM!!!")

        elif state == State.ALARM_TIME:
            self.display.as_clock(self.alarm_settings.time, "SET TIME")

        else:
            log.error('Unknown state %s', state)

    def btn_up_cb(self):
        self.alarm_settings.up()
        self.alarm_settings.set()
        self.state.set_alarm_time()
        self.refresh_display()

    def btn_down_cb(self):
        self.alarm_settings.down()
        self.alarm_settings.set()
        self.state.set_alarm_time()
        self.refresh_display()

    def btn_onoff_cb(self):
        self.alarm_settings.toggle()
        self.refresh_display()

    def btn_snooze_cb(self):
        self.alarm.ack()
        self.refresh_display()
