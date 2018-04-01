from .leds import RGBLeds
from . import colors


class Light:
    def __init__(self):
        self._leds = RGBLeds(24)

    def off(self):
        self._leds.set_all(colors.Off)
        self._leds.refresh()

    def on(self):
        self._leds.set_all(colors.On)
        self._leds.refresh()

    def set_alarm(self, progression):
        brightness = min(1, progression * 2)
        self._leds.set_white(4000, brightness)
        self._leds.refresh()

    def unset_alarm(self):
        self.off()

    def close(self):
        self.off()
        self._leds.close()
