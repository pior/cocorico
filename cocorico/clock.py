import datetime

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
            et = self.effective_time
            if self._clock.now > et:
                self._triggered = True
        return self._triggered

    def ack(self):
        self._ack_time = self._clock.now
        self._triggered = False


class AlarmSettings:
    def __init__(self, increment=1):
        soonish = Clock().now + datetime.timedelta(minutes=2)
        self._time = (soonish.hour, soonish.minute)  # For testing, set it soonish

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

    def with_values(self, **kwargs):
        return self.now.replace(**kwargs)
