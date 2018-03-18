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
        log.info("writing: %s", data)


if SpiDev is None:
    SpiDev = MockSpiDev
    log.info("Using SpiDev mock")
