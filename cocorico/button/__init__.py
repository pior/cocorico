import logging
import threading
import time

from cocorico.hal.gpio import GPIO

log = logging.getLogger(__name__)


class Button:
    """
    Call a function when a (active low) button is pressed.
    With interrupt and software debouncing.

    Debouncing strategy:
    - block interrupt for 200ms using the RPi.GPIO bouncetime parameter
    - read the input multiple times
    - call function if all reads return active.
    """

    def __init__(self, pin, callback):
        self._pin = pin
        self._callback = callback

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self._gpio_callback, bouncetime=50)

        self._in_interrupt = False

    def _pressed(self):
        return GPIO.input(self._pin) == GPIO.LOW

    def _gpio_callback(self, channel):
        log.info("%r: event channel=%s", self, channel)

        if self._in_interrupt:
            log.info("%r: ignore interrupt during interrupt handling", self)
            return

        self._in_interrupt = True
        try:
            for _ in range(10):
                # time.sleep(0.001)
                if not self._pressed():
                    log.info("%r: ignore bounce", self)
                    return
        finally:
            self._in_interrupt = False

        self._call_callback()

    def _call_callback(self):
        log.info("%r: calling %s", self, self._callback)
        self._callback()


    def __repr__(self):
        return "Button(pin=%s)" % self._pin
