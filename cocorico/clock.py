import datetime

import pytz


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
        return self.time.strftime("%H:%S")
