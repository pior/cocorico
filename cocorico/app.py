import atexit
import time
import logging

from .button import Button
from .clock import Alarm, AlarmSettings, Clock
from .display import Display
from .light import Light
from .lux import Lux
from .sound import Sound
from .state import State

log = logging.getLogger(__name__)


class App():
    def __init__(self):
        log.info('Initializing...')
        self.display = Display()
        self.sound = Sound()
        self.light = Light()
        self.lux = Lux()

        self.ui_state = State()
        self.clock = Clock()
        self.alarm_settings = AlarmSettings()
        self.alarm = Alarm(clock=self.clock, settings=self.alarm_settings)

        self.btn_up = Button(pin=23, callback=self.action_up)
        self.btn_down = Button(pin=22, callback=self.action_down)
        self.btn_onoff = Button(pin=17, callback=self.action_onoff)
        self.btn_stop = Button(pin=27, callback=self.action_stop)
        self.btn_snooze = Button(pin=26, callback=self.action_snooze)
        log.info('Initialized.')

    def close(self):
        log.info('Closing...')
        self.sound.close()
        self.light.close()
        self.display.close()

    def routine(self, time_previous, time_now):
        """Called each second to refresh the application state."""

        if time_previous is None:
            self.light.off()
            self.sound.play_startup()
            return

        if self.alarm.triggered:
            log.info('Triggered!')
            self.ui_state.set_alarm()

        self.sound.refresh()
        self.ui_refresh()

        log.info("%s", self.lux)

    def ui_refresh(self):
        state = self.ui_state.get()
        log.info('State = %s', state)

        if state == State.CLOCK:  # STANDBY
            if self.alarm_settings.active:
                alarm_time = self.alarm_settings.time.strftime('%H:%M')
                text = '     %s' % alarm_time
            else:
                text = ''
            self.display.as_clock(self.clock.time, text)
            self.light.unset_alarm()
            self.sound.unset_alarm()
            if self.lux.is_dark:
                self.display.hide()
            else:
                self.display.show()

        elif state == State.ALARM:
            self.display.as_clock(self.clock.time, ' /!\ ALARM /!\\')
            self.sound.set_alarm()
            self.light.set_alarm()

        elif state == State.ALARM_TIME:
            self.display.as_clock(self.alarm_settings.time, 'SET TIME')

        else:
            log.error('Unknown state %s', state)

    def do_alarm_ack(self):
        self.alarm.ack()
        self.ui_state.set_clock()
        self.ui_refresh()

    def action_up(self):
        if self.ui_state.is_alarm():
            self.do_alarm_ack()
            return
        self.alarm_settings.up()
        self.alarm_settings.set()
        self.ui_state.set_alarm_time()
        self.ui_refresh()

    def action_down(self):
        if self.ui_state.is_alarm():
            self.do_alarm_ack()
            return
        self.alarm_settings.down()
        self.alarm_settings.set()
        self.ui_state.set_alarm_time()
        self.ui_refresh()

    def action_onoff(self):
        if self.ui_state.is_alarm():
            self.do_alarm_ack()
            return
        self.alarm_settings.toggle()
        self.ui_refresh()

    def action_stop(self):
        if self.ui_state.is_alarm():
            self.do_alarm_ack()
            return

    def action_snooze(self):
        if self.ui_state.is_alarm():
            self.do_alarm_ack()
            return
