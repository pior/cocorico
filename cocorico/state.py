import time


class State:
    STANDBY = 'standby'
    ALARM = 'alarm'
    ALARM_TIME = 'alarm_time'

    def __init__(self):
        self._state = self.STANDBY
        self._state_progression = self.STANDBY
        self._until = None

    def _set(self, state, seconds=None, progression=None):
        self._state = state
        self._state_progression = progression
        self._until = (time.time() + seconds) if seconds else None

    def _check_timer(self):
        if self._until is not None and time.time() > self._until:
            self._set(self.STANDBY)

    def get(self):
        self._check_timer()
        return self._state, self._state_progression

    def set_standby(self):
        self._set(self.STANDBY)

    def set_alarm(self, progression):
        self._set(self.ALARM, progression=progression)

    def set_alarm_time(self):
        self._set(self.ALARM_TIME, 2)

    def is_alarm(self):
        return self._state == self.ALARM
