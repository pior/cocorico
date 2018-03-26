import logging

log = logging.getLogger(__name__)


class MockGPIO:
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self._class_state)

    _mode = None
    BCM = 'BCM'

    @classmethod
    def setmode(cls, mode):
        cls._mode = mode

    _setup = {}
    IN = 'IN'
    OUT = 'OUT'
    PUD_UP = 'PUD_UP'
    PUD_DOWN = 'PUD_DOWN'
    LOW = 'LOW'
    HIGH = 'HIGH'

    @classmethod
    def setup(cls, pin, direction, pull_up_down=None, initial=None):
        cls._setup[pin] = (direction, pull_up_down, initial)

    @classmethod
    def cleanup(cls, pin=None):
        pass

    _event_to_detect = []
    FALLING = 'FALLING'

    @classmethod
    def add_event_detect(cls, pin, event_type, callback=None, bouncetime=None):
        cls._event_to_detect.append((pin, event_type, callback, bouncetime))

    _inputs_values = {}

    @classmethod
    def input(cls, pin):
        return cls._inputs_values[pin].pop()

    @classmethod
    def _mock_set_input_values(cls, pin, values):
        cls._inputs_values[pin] = list(values)

    _outputs_values = {}

    @classmethod
    def output(cls, pin, state):
        cls._outputs_values[pin] = state


try:
    import RPi.GPIO as GPIO
except ImportError:
    log.warning("Using RPi.GPIO mock")
    GPIO = MockGPIO

GPIO.setmode(GPIO.BCM)
