from .leds import RGBLeds
from . import colors


class Light:
    def __init__(self):
        self._leds = RGBLeds(24)
        self.off()
        # self._wheel = wheel()

    # def refresh(self):
    #     new_color = next(self._wheel)
    #     self._leds.set_all(new_color)
    #     self._leds.refresh()

    def off(self):
        self._leds.set_all(colors.Off)
        self._leds.refresh()

    def on(self):
        self._leds.set_all(colors.On)
        self._leds.refresh()

    def close(self):
        self.off()
