import time
import signal
import typing
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info('gpiozero is loading...')
import gpiozero
log.info('gpiozero loaded')


class App():
    def __init__(self):
        log.info('Application initializing...')
        self.led1 = gpiozero.LED(22)
        self.led2 = gpiozero.LED(23)
        log.info('Application initialized.')

    def run(self):
        log.info('Application running...')
        self.loop()

    def loop(self):
        state = False

        while True:
            state = not state
            self.led1.value = state
            self.led2.value = not state
            time.sleep(0.2)
