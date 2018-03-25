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
        data += [0x00] * 3  # Commit sequecnce: words with MSB cleared
        self._spi.xfer(data)

    # def set_pixel(self, pixel, color):
    #     if 0 <= pixel < self._led:
    #         self._pixel_buffer[pixel * 3: (pixel + 1) * 3] = color_to_lpd8806(color)
    #     else:
    #         log.info('Invalid pixel %s on %s strip', pixel, self._led)

    def set_all(self, color):
        self._pixel_buffer = [color] * self._led_count
