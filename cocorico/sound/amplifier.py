from cocorico.hal.gpio import GPIO


class Amplifier:
    SHUTDOWN_PIN = 4  # BCM pin 4

    def __init__(self):
        GPIO.setup(self.SHUTDOWN_PIN, GPIO.OUT, initial=GPIO.LOW)
        self._shutdown = False

    def enable(self):
        if self._shutdown:
            GPIO.output(self.SHUTDOWN_PIN, GPIO.HIGH)
            self._shutdown = False

    def disable(self):
        if not self._shutdown:
            GPIO.output(self.SHUTDOWN_PIN, GPIO.LOW)
            self._shutdown = True
