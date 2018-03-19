import time


class State:
    CLOCK = 'clock'
    ALARM = 'alarm'
    ALARM_TIME = 'alarm_time'

    def __init__(self):
        self._state = self.CLOCK
        self._until = 0

    def _set(self, state, seconds=0):
        self._state = state
        self._until = time.time() + seconds

    def get(self):
        if self._state != self.CLOCK and time.time() > self._until:
            self._state = self.CLOCK
        return self._state

    def set_clock(self):
        self._set(self.CLOCK)

    def set_alarm(self):
        self._set(self.ALARM, 3)

    def is_alarm(self):
        return self._state == self.ALARM

    def set_alarm_time(self):
        self._set(self.ALARM_TIME, 2)
