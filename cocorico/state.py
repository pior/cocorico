import time


class State:
    STANDBY = 'standby'
    ALARM = 'alarm'
    ALARM_TIME = 'alarm_time'

    def __init__(self):
        self._state = self.STANDBY
        self._until = None

    def _set(self, state, seconds=None):
        self._state = state
        if seconds:
            self._until = time.time() + seconds

    def _check_timer(self):
        if self._until is not None and time.time() > self._until:
            self._state = self.STANDBY
            self._until = None

    def get(self):
        self._check_timer()
        return self._state

    def set_standby(self):
        self._set(self.STANDBY)

    def set_alarm(self):
        self._set(self.ALARM)

    def set_alarm_time(self):
        self._set(self.ALARM_TIME, 2)

    def is_alarm(self):
        return self._state == self.ALARM
