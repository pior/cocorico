import atexit
import logging
import os
import select
import sys
import termios
import tty

from cocorico.utils import PeriodicTask

log = logging.getLogger(__name__)


class MockButton:
    _buttons = None

    def __init__(self, callback):
        if self._buttons is None:
            self._buttons = MockButtons()
        self._buttons.bind(callback)


class MockButtons:
    _keys_available = list(b'qwertyuiop')
    _callback_map = {}

    def __init__(self):
        self._keyboard_spy = KeyboardSpy()
        self._thread = PeriodicTask(1, self.poll)
        self._thread.start()

    @classmethod
    def bind(cls, callback):
        key = cls._keys_available.pop(0)

        log.info('Bound mockbutton on %s to %s', key, callback)
        cls._callback_map[key] = callback

    def poll(self):
        key = self._keyboard_spy.read()

        if not key:
            return

        callback = self._callback_map.get(ord(key))
        if callback is None:
            log.error("Detected key %s without bound callback: %s", key, self._callback_map)
        else:
            log.error("Detected key %s, calling callback %s", key, callback)
            callback()


class KeyboardSpy:
    _saved_attributes = None

    def __init__(self):
        if self._saved_attributes is None:
            self._global_init()
            atexit.register(self._reset)

    @classmethod
    def _global_init(cls):
        cls._saved_attributes = termios.tcgetattr(sys.stdin)

        attrs = termios.tcgetattr(sys.stdin)
        attrs[3] = attrs[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, attrs)

    def _reset(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._saved_attributes)

    def read(self):
        try:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return os.read(sys.stdin.fileno(), 1)
        except OSError:
            pass
