import logging

log = logging.getLogger(__name__)


class MockSMBus:
    def __init__(self, bus):
        self._bus = bus

    def write_byte_data(self, i2c_addr, register, value):
        log.debug("write_byte_data: i2c_addr=%s register=%s value=%s", i2c_addr, register, value)

    def read_word_data(self, i2c_addr, register):
        log.debug("read_word_data: i2c_addr=%s register=%s", i2c_addr, register)
        return 10

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__dict__)


try:
    from smbus2 import SMBus
except ImportError:
    log.warning("Using I2C mock")
    SMBus = MockSMBus
