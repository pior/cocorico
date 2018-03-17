import time

import RPIO

GPIO_LED_1 = 22
GPIO_LED_2 = 23


def main():
    RPIO.setup(GPIO_LED_1, RPIO.OUT, initial=RPIO.LOW)
    RPIO.setup(GPIO_LED_2, RPIO.OUT, initial=RPIO.LOW)

    state = False
    while True:
        state = not state

        RPIO.output(GPIO_LED_1, state)
        RPIO.output(GPIO_LED_2, not state)

        time.sleep(0.2)

main()
