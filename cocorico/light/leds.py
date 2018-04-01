import time
import logging

from cocorico.hal.spi import SpiDev
from . import colors

log = logging.getLogger(__name__)


def color_to_lpd8806(color):
    return [(x >> 1)  | 0x80 for x in color.raw]


class RGBLeds:
    def __init__(self, led_count):
        self._spi = SpiDev()
        self._spi.open(1, 0)
        self._spi.max_speed_hz = 4_000_000

        self._led_count = led_count
        self._pixel_buffer = [colors.Black] * led_count

    def refresh(self):
        data = [
            byte
            for pixel in self._pixel_buffer
            for byte in color_to_lpd8806(pixel)
        ]
        data += [0x00] * 3  # Commit sequence: words with MSB cleared
        self._spi.xfer(data)

    def set_all(self, color):
        self._pixel_buffer = [color] * self._led_count

    def set_white(self, kelvin, brightness):
        color = colors.from_kelvin(kelvin, brightness)
        log.info("Set white: kelvin=%s brightness=%s color=%s", kelvin, brightness, color)
        self.set_all(color)

    def close(self):
        self._spi.close()
