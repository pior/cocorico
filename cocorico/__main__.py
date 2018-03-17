import time

import gpiozero


LED1 = gpiozero.LED(22)
LED2 = gpiozero.LED(23)


def main():
    state = False

    while True:
        state = not state
        LED1.value = state
        LED2.value = not state
        time.sleep(0.2)


main()
