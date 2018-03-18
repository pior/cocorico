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
    - read the input 3 times
    - call function if 3 reads return active.
    """

    def __init__(self, pin, callback, callback_args=None, callback_kwargs=None):
        self._pin = pin
        self._callback = callback
        self._callback_args = callback_args
        self._callback_kwargs = callback_kwargs

        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self._gpio_callback, bouncetime=200)

    def _is_active(self):
        return GPIO.input(self._pin) == GPIO.LOW

    def _gpio_callback(self, channel):
        log.info("%r: event channel=%s", self, channel)

        # Stupid debouncing for a start (blocking for 10ms)
        for x in range(2):
            time.sleep(0.005)
            if not self._is_active():
                log.info("%r: ignore bounce", self)
                break
        else:
            log.info("%r: calling %s(%s, %s)", self, self._callback, self._callback_args, self._callback_kwargs)
            self._callback(*self._callback_args, **self._callback_kwargs)


    def __repr__(self):
        return "Button(pin=%s)" % self._pin