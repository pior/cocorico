import datetime
from typing import NamedTuple

import pytz


class Alarm:
    DETECTION_PERIOD = datetime.timedelta(minutes=1)

    def __init__(self, clock, settings):
        self._settings = settings
        self._clock = clock
        self._triggered = False
        self._ack_time = clock.now

    @property
    def effective_time(self):
        now = self._clock.now

        alarm_time = self._settings.time
        alarm_datetime = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=0, microsecond=0)

        threshold = alarm_datetime + datetime.timedelta(minutes=1)  # Give us a minute to call triggered()
        if self._ack_time > alarm_datetime:
            threshold = min(threshold, self._ack_time)  # If acked, effective time jump to next cycle

        if now > threshold:
            alarm_datetime += datetime.timedelta(hours=24)

        return alarm_datetime

    @property
    def triggered(self):
        if not self._settings.active:
            self._triggered = False
        elif not self._triggered:
            if self._clock.now > self.effective_time:
                self._triggered = True
        return self._triggered

    @property
    def rampup_position(self, rampup_time=300):
        if not self.triggered:
            return
        elapsed = self._clock.now - self.effective_time
        return min(1, elapsed.total_seconds() / rampup_time)

    def ack(self):
        self._ack_time = self._clock.now
        self._triggered = False


class CyclicTime:
    def __init__(self, hour, minute):
        self.hour = hour
        self.minute = minute

    @classmethod
    def create_from(cls, other):
        return cls(other.hour, other.minute)

    def copy_from(self, other):
        self.hour, self.minute = other.hour, other.minute

    def as_time(self):
        return datetime.time(hour=self.hour, minute=self.minute)

    def relative_set(self, delta_minutes, step_minutes):
        assert delta_minutes <= 60, 'Not supporting more than 60min of increment'

        minute = self.minute + delta_minutes
        hour = self.hour
        if minute >= 60:
            hour += 1
        if minute < 0:
            hour -= 1
        self.minute = ((minute % 60) // step_minutes) * step_minutes
        self.hour = hour % 24


class AlarmSettings:
    def __init__(self, increment=10):
        soonish = Clock().now + datetime.timedelta(minutes=2)
        self._time = CyclicTime.create_from(soonish)  # For testing, set it soonish

        self._time_update = CyclicTime.create_from(self._time)
        self._increment = increment
        self.active = True

    def toggle(self):
        self.active = not self.active

    @property
    def time(self):
        return self._time.as_time()

    @property
    def time_update(self):
        return self._time_update.as_time()

    def up(self):
        self._time_update.relative_set(self._increment, self._increment)

    def down(self):
        self._time_update.relative_set(-self._increment, self._increment)

    def set(self):
        self._time.copy_from(self._time_update)


class Clock:
    def __init__(self):
        self.tz = pytz.timezone('America/Toronto')

    @property
    def now(self):
        return datetime.datetime.now(self.tz)

    @property
    def time(self):
        return self.now.time()

    @property
    def time_str(self):
        return _time_format(self.time)

    def with_values(self, **kwargs):
        return self.now.replace(**kwargs)
