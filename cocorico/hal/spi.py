import logging

log = logging.getLogger(__name__)


class MockSpiDev:
    def open(self, port, device):
        log.info("SPI open port=%s device=%s", port, device)

    def xfer(self, data):
        log.info("%r: Transaction: %s", self, ' '.join('%0.2X' % n for n in data))

    def writebytes(self, data):
        log.info("%r: Writes: %s", self, ' '.join('%0.2X' % n for n in data))

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__dict__)


try:
    from spidev import SpiDev
except ImportError:
    log.warning("Using SpiDev mock")
    SpiDev = MockSpiDev
