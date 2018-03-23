from .leds import RGBLeds
from .colors import wheel


class Light:
    def __init__(self):
        self._leds = RGBLeds(24)
        self._wheel = wheel()

    def refresh(self):
        new_color = next(self._wheel)
        self._leds.set_all(new_color)
        self._leds.refresh()
