import logging

log = logging.getLogger(__name__)


try:
    from spidev import SpiDev
except ImportError:
    SpiDev = None


class MockSpiDev:
    def open(self, port, device):
        log.info("SPI open port=%s device=%s", port, device)

    def xfer(self, data):
        log.info("%r: %s", self, data)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__dict__)


if SpiDev is None:
    SpiDev = MockSpiDev
    log.info("Using SpiDev mock")
