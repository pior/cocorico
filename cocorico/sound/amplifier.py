import logging

from cocorico.hal.gpio import GPIO

log = logging.getLogger(__name__)


class Amplifier:
    SHUTDOWN_PIN = 4  # BCM pin 4
    ENABLED = GPIO.LOW
    DISABLE = GPIO.HIGH

    def __init__(self):
        GPIO.setup(self.SHUTDOWN_PIN, GPIO.OUT, initial=self.DISABLE)


    def enable(self):
        log.info("Enable amplifier")
        GPIO.output(self.SHUTDOWN_PIN, self.ENABLE)

    def disable(self):
        log.info("Disable amplifier")
        GPIO.output(self.SHUTDOWN_PIN, self.DISABLE)

    def close(self):
        GPIO.cleanup(self.SHUTDOWN_PIN)
