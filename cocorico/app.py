import time
import logging

from .light import Light
from .display import Display
from .sound import Sound
from .state import State
from .button import Button
from .clock import Alarm, AlarmSettings, Clock

log = logging.getLogger(__name__)


class App():
    def __init__(self):
        log.info('Initializing...')
        self.display = Display()
        self.sound = Sound()
        self.light = Light()

        self.state = State()
        self.clock = Clock()
        self.alarm_settings = AlarmSettings()
        self.alarm = Alarm(clock=self.clock, settings=self.alarm_settings)

        self.btn_up = Button(pin=23, callback=self.action_up)
        self.btn_down = Button(pin=22, callback=self.action_down)
        self.btn_onoff = Button(pin=17, callback=self.action_onoff)
        self.btn_snooze = Button(pin=27, callback=self.action_snooze)
        log.info('Initialized.')

    def run(self):
        log.info('Running...')

        self.sound.play_startup()

        while True:
            self.periodic_routine()
            time.sleep(1)

    def periodic_routine(self):
        # self.sound.shutdown_if_possible()

        if self.alarm.triggered:
            log.info('Triggered!')
            self.state.set_alarm()

        self.light.refresh()
        self.sound.refresh()
        self.refresh()

    def refresh(self):
        state = self.state.get()
        log.info('State = %s', state)

        if state == State.CLOCK:  # STANDBY
            if self.alarm_settings.active:
                alarm_time = self.alarm_settings.time.strftime('%H:%M')
                text = '     %s' % alarm_time
            else:
                text = ''
            self.display.as_clock(self.clock.time, text)

        elif state == State.ALARM:
            self.display.as_clock(self.clock.time, ' /!\ ALARM /!\\')
            self.sound.play_alarm()

        elif state == State.ALARM_TIME:
            self.display.as_clock(self.alarm_settings.time, 'SET TIME')

        else:
            log.error('Unknown state %s', state)

    def do_alarm_ack(self):
        self.sound.stop()
        self.alarm.ack()
        self.state.set_clock()
        self.refresh()

    def action_up(self):
        if self.state.is_alarm():
            self.do_alarm_ack()
            return
        self.alarm_settings.up()
        self.alarm_settings.set()
        self.state.set_alarm_time()
        self.refresh()

    def action_down(self):
        if self.state.is_alarm():
            self.do_alarm_ack()
            return
        self.alarm_settings.down()
        self.alarm_settings.set()
        self.state.set_alarm_time()
        self.refresh()

    def action_onoff(self):
        if self.state.is_alarm():
            self.do_alarm_ack()
            return
        self.alarm_settings.toggle()
        self.refresh()

    def action_snooze(self):
        if self.state.is_alarm():
            self.do_alarm_ack()
            return
