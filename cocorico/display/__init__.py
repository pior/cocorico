from luma.core.interface.serial import spi as luma_spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

from cocorico.hal.spi import SpiDev
from cocorico.hal.gpio import GPIO


def test(text="Hello World"):
    GPIO.setmode(GPIO.BCM)
    serial = luma_spi(spi=SpiDev(), gpio=GPIO, device=0, port=0)
    device = ssd1306(serial)

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 40), text, fill="white")
