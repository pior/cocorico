import time
import logging

# import gpiozero
from . import hal

log = logging.getLogger(__name__)


# def blinking_led_loop():
#     led1 = gpiozero.LED(22)
#     led2 = gpiozero.LED(23)

#     state = False

#     while True:
#         state = not state
#         # print(state)
#         led1.value = state
#         led2.value = not state
#         time.sleep(0.2)


class RGBLeds:
    END_SEQUENCE = [0x00, 0x00, 0x00]

    def __init__(self, led=8, speed=1_000_000):
        self._spi = hal.SpiDev()
        self._spi.open(0, 0)
        self._spi.max_speed_hz = speed

        self._led = led
        self._buffer = [0x00, 0x00, 0x00] * led

    def refresh(self):
        self._spi.xfer(self._buffer + self.END_SEQUENCE)

    def set_pixel(self, pixel, color):
        if 0 <= pixel < self._led:
            self._buffer[pixel * 3: (pixel + 1) * 3] = color
        else:
            log.info('Invalid pixel %s on %s strip', pixel, self._led)

    def set_all(self, color):
        for pixel in range(self._led):
            self.set_pixel(pixel, color)

    def test(self):
        for color in [
            (0x00, 0x00, 0x00),
            (0x40, 0x40, 0x40),
            (0x80, 0x80, 0x80),
            (0xA0, 0xA0, 0xA0),
            (0xFF, 0xFF, 0xFF),
            (0xFF, 0x00, 0x00),
            (0x00, 0xFF, 0x00),
            (0x00, 0x00, 0xFF),
        ]:
            log.info('Color %s', color)
            self.set_all(color)
            self.refresh()
            time.sleep(1)
