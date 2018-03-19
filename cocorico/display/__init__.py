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
        self._text_font = ImageFont.truetype('fonts/digital-7-mono.ttf', 10)

    # def announce(self, text):
    #     with canvas(self._device) as draw:
    #         draw.rectangle(self._device.bounding_box, outline="white", fill="black")
    #         draw.text((30, 25), text, font=self._large_font, fill="white")

    def as_clock(self, time):
        text = _format_time(time)
        log.info("Clock: %s", text)

        with canvas(self._device) as draw:
            draw.text((0, 0), text, font=self._clock_font, fill="white")

    def as_set_alarm(self, time):
        text = _format_time(time)
        log.info("Set alarm: %s", text)

        with canvas(self._device) as draw:
            draw.text((0, 0), text, font=self._clock_font, fill="white")
            draw.text((0, 42), "SET ALARM TIME", font=self._text_font, fill="white")
