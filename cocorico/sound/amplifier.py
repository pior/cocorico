import logging

from cocorico.hal.gpio import GPIO

log = logging.getLogger(__name__)


class Amplifier:
    SHUTDOWN_PIN = 4  # BCM pin 4

    def __init__(self):
        self.disable()

    def enable(self):
        log.info("Enable amplifier")
        GPIO.setup(self.SHUTDOWN_PIN, GPIO.IN)  # High impedance (pullup on 5v on amp board)

    def disable(self):
        log.info("Disable amplifier")
        GPIO.setup(self.SHUTDOWN_PIN, GPIO.OUT, initial=GPIO.LOW)  # Force low

    def close(self):
        GPIO.cleanup(self.SHUTDOWN_PIN)  # amp will be left "active"
