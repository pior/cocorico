from cocorico.hal.i2c import SMBus
from cocorico.lib.tsl2591 import Tsl2591
from cocorico.utils import PeriodicTask


class Lux:
    def __init__(self):
        self._sensor = Tsl2591(SMBus(1))
        self._setvalue(0)
        PeriodicTask(0.5, self._poll).start()

    def _read(self):
        full, ir = self._sensor.get_full_luminosity()
        lux = self._sensor.calculate_lux(full, ir)
        return lux

    def _setvalue(self, lux):
        self.lux = lux
        self.is_dark = lux < 1
        self.is_lighted = lux > 5


    def _poll(self):
        self._setvalue(self._read())


    def __repr__(self):
        return f'<Lux lux={self.lux} is_dark={self.is_dark} is_lighted={self.is_lighted}>'
