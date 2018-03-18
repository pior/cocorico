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

    # OUT = 'OUT'
    # LOW = 'LOW'

    # def __init__(self, *args, **kwargs):
    #     self.__init_args = (args, kwargs)
    #     self.__object_state = {}

    # @classmethod
    # def __getattr__(cls, name):
    #     import pdb; pdb.set_trace()
    #     if name.isupper():
    #         return name
    #     else:
    #         return super().__getattr__(name)

    # @classmethod
    # def setmode(self, *args, **kwargs):
    #     self.__class_state['setmode'] = (args, kwargs)

    # @classmethod
    # def setup(self, *args, **kwargs):
    #     self.__class_state['setup'] = (args, kwargs)

    # @classmethod
    # def setup(self, *args, **kwargs):
    #     self.__class_state['setup'] = (args, kwargs)

    # def __repr__(self):
    #     state = self.__dict__.copy()
    #     state.update(self.__class_state)
    #     state.update(self.__object_state)
    #     return "%s(%s)" % (self.__class__.__name__, state)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self._class_state)



try:
    import RPi.GPIO as GPIO
except ImportError:
    log.warning("Using RPi.GPIO mock")
    GPIO = MockGPIO
