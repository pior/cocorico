import time

import gpiozero
import spidev


def blinking_led_loop():
    led1 = gpiozero.LED(22)
    led2 = gpiozero.LED(23)

    state = False

    while True:
        state = not state
        # print(state)
        led1.value = state
        led2.value = not state
        time.sleep(0.2)


class RGBLeds:
    def __init__(self):
        self._spi = spidev.SpiDev()
        self._spi.open(0, 0)
        self._spi.max_speed_hz = 4_000_000

    def test(self):
        buffer = [0x80, 0x80, 0x80] * 4
        buffer += [0x00, 0x00, 0x00]  # "push" the bits and make sure no glitch color appear
        self._spi.xfer(buffer)
