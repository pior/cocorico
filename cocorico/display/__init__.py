import time
import logging

from luma.core.interface.serial import spi as luma_spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

from PIL import ImageFont

from cocorico.hal.spi import SpiDev
from cocorico.hal.gpio import GPIO

log = logging.getLogger(__name__)


def _format_time(time):
    return time.strftime("%H:%M")


class Display:

    def __init__(self):
        serial = luma_spi(spi=SpiDev(), gpio=GPIO, device=0, port=0)
        self._device = ssd1306(serial)

        self._clock_font = ImageFont.truetype('fonts/digital-7-mono.ttf', 56)
        self._text_font = ImageFont.truetype('fonts/digital-7-mono.ttf', 18)

    def as_clock(self, time, subtext=None):
        text = _format_time(time)

        log.info("Clock: %s (%s)", text, subtext)

        with canvas(self._device) as draw:
            draw.text((0, 0), text, font=self._clock_font, fill="white")
            draw.text((0, 42), subtext, font=self._text_font, fill="white")

    def show(self):
        self._device.show()

    def hide(self):
        self._device.hide()

    def close(self):
        self._device.clear()
