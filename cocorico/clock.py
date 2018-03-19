import datetime

import pytz


class Alarm:
    TRIGGER_PERIOD = datetime.timedelta(minutes=10)

    def __init__(self, clock, settings):
        self._settings = settings
        self._clock = clock
        self._triggered = False
        self._last_ack = clock.now

    @property
    def next_alarm_time(self):
        now = self._clock.now

        t = self._settings.time
        alarm_time = self._clock.now.replace(hour=t.hour, minute=t.minute)

        safe_limit = now + self.TRIGGER_PERIOD
        guard_time_for_today_alarm = max(safe_limit, self._last_ack)

        if alarm_time < guard_time_for_today_alarm:
            return alarm_time
        else:
            return alarm_time + datetime.timedelta(hours=24)

    @property
    def seconds_to_next_alarm(self):
        return (self.next_alarm_time - self._clock.now).total_seconds()

    @property
    def triggered(self):
        if not self._triggered and (self.next_alarm_time < self._clock.now):
            self._triggered = True
        return self._triggered

    def ack(self):
        self._last_ack = self._clock.now
        self._triggered = False


class AlarmSettings:
    def __init__(self, increment=1):
        self._time = (23, 24)
        self._time_update = self._time
        self._increment = min(60, increment)  # > 60 is not supported
        self.active = True

    def toggle(self):
        self.active = not self.active

    @property
    def time(self):
        return datetime.time(hour=self._time[0], minute=self._time[1])

    @property
    def time_update(self):
        return datetime.time(hour=self._time_update[0], minute=self._time_update[1])

    def up(self):
        hour, minute = self._time_update
        minute = minute + self._increment
        if minute >= 60:
            hour += 1
        self._time_update = (hour % 60, minute % 60)

    def down(self):
        hour, minute = self._time_update
        minute -= self._increment
        if minute < 0:
            hour -= 1
            minute += 60
        if hour < 0:
            hour += 23
        self._time_update = (hour, minute)

    def set(self):
        self._time = self._time_update


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
