from cocorico.hal.i2c import SMBus
from cocorico.lib.tsl2591 import Tsl2591
from cocorico.utils import PeriodicTask


class Lux:
    def __init__(self):
        self._sensor = Tsl2591(SMBus(1))
        self.is_dark = False
        self.is_lighted = False
        PeriodicTask(0.5, self._poll)

    def _read(self):
        full, ir = self._sensor.get_full_luminosity()
        lux = self._sensor.calculate_lux(full, ir)
        return lux

    def _poll(self):
        lux = self._read()
        self.is_dark = lux < 1
        self.is_lighted = lux > 5

    def __repr__(self):
        return f'<Lux is_dark={self.is_dark} is_lighted={self.is_lighted}>'
