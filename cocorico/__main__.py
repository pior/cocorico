import time

import gpiozero


LED1 = gpiozero.LED(22)
LED1 = gpiozero.LED(23)


def main():
    LED1.toggle()

    while True:
        LED1.toggle()
        LED2.toggle()
        time.sleep(0.2)


main()
