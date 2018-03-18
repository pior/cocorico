import logging

log = logging.getLogger(__name__)

try:
    from spidev import SpiDev
except ImportError:
    log.warning("Using SpiDev mock")
    from .spi import MockSpiDev as SpiDev
