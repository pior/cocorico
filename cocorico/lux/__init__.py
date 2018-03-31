from cocorico.hal.i2c import SMBus
from cocorico.lib.tsl2591 import Tsl2591


class Lux:
    def __init__(self):
        bus = SMBus(1)
        self._sensor = Tsl2591(bus)

    def read(self):
        full, ir = self._sensor.get_full_luminosity()
        lux = self._sensor.calculate_lux(full, ir)
        return lux
