from cocorico.hal.gpio import GPIO


class Amplifier:
    SHUTDOWN_PIN = 4  # BCM pin 4

    def __init__(self):
        GPIO.setup(self.SHUTDOWN_PIN, GPIO.OUT, initial=GPIO.HIGH)
        self._active = False

    def enable(self):
        if not self._active:
            GPIO.output(self.SHUTDOWN_PIN, GPIO.LOW)
            self._active = True

    def disable(self):
        if self._active:
            GPIO.output(self.SHUTDOWN_PIN, GPIO.HIGH)
            self._active = False

    def close(self):
        GPIO.cleanup(self.SHUTDOWN_PIN)
