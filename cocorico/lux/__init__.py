from cocorico.hal.i2c import SMBus
from cocorico.lib.tsl2591 import Tsl2591
from cocorico.utils import PeriodicTask


class Lux:
    def __init__(self):
        self._sensor = Tsl2591(SMBus(1))
        self._setvalue(0)
        self._thread = PeriodicTask(0.5, self._poll)
        self._thread.start()

    def close(self):
        self._thread.stop()
        self._thread.join()

    def _poll(self):
        self._setvalue(self._sensor.measure_lux())

    def _setvalue(self, lux):
        self.lux = lux
        self.is_dark = lux < 1
        self.is_lighted = lux > 5

    def __repr__(self):
        return '<Lux lux=%.3f is_dark=%s is_lighted=%s>' % (self.lux, self.is_dark, self.is_lighted)
