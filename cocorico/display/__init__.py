from luma.core.interface.serial import spi as luma_spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

from cocorico.hal.spi import SpiDev
from cocorico.hal.gpio import GPIO


class Display:

    def __init__(self):
        serial = luma_spi(spi=SpiDev(), gpio=GPIO, device=0, port=0)
        self._device = ssd1306(serial)

    def announce(self, text):
        with canvas(self._device) as draw:
            draw.rectangle(self._device.bounding_box, outline="white", fill="black")
            draw.text((30, 25), text, fill="white")
