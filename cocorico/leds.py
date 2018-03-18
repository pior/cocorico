import time
import logging

# import gpiozero
import spidev

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
    def __init__(self, speed=1_000_000):
        self._spi = spidev.SpiDev()
        self._spi.open(0, 0)
        self._spi.max_speed_hz = speed

    def test(self):
        for update_func in [self._update_1, self._update_2]:
            log.info('With %s', update_func)

            for data in [
                [[0x00, 0x00, 0x00]],
                [[0x00, 0x00, 0x00]] * 4,
                [[0x00, 0x00, 0x00]] * 8,

                [[0x80, 0x80, 0x80]],
                [[0x80, 0x80, 0x80]] * 4,
                [[0x80, 0x80, 0x80]] * 8,

                [[0xFF, 0xFF, 0xFF]],
                [[0xFF, 0xFF, 0xFF]] * 4,
                [[0xFF, 0xFF, 0xFF]] * 8,

                [[0xFF, 0x00, 0x00]] * 8,
                [[0x00, 0xFF, 0x00]] * 8,
                [[0x00, 0x00, 0xFF]] * 8,
            ]:
                log.info('Pushing %s', data)
                update_func(data)
                time.sleep(1)

    def _update_1(self, buffer):
        for chunk in buffer + [[0x00, 0x00, 0x00]]:
            self._spi.xfer(chunk)

    def _update_2(self, buffer):
        for chunk in buffer + [[0x00, 0x00, 0x00]]:
            self._spi.xfer2(chunk)
