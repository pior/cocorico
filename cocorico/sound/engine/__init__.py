import logging

log = logging.getLogger(__name__)


def build():
    try:
        from .alsa import AlsaPlayer as Player
    except ImportError:
        from .afplay import Afplay as Player

    log.info("Sound engine: %r", Player)
    return Player()
