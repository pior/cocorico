import logging

log = logging.getLogger(__name__)


class AutoConstants(type):
    def __getattr__(self, name):
        if name.isupper():  # Let's constants be constant
            return name
        else:
            def action_func(*args, **kwargs):
                self._class_state[name] = (args, kwargs)
                log.info("MockGPIO: %s(%s, %s)", name, args, kwargs)
            return action_func


class MockGPIO(metaclass=AutoConstants):
    _class_state = {}

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self._class_state)

try:
    import RPi.GPIO as GPIO
except ImportError:
    log.warning("Using RPi.GPIO mock")
    GPIO = MockGPIO

GPIO.setmode(GPIO.BCM)
