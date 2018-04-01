'''
Copied from https://github.com/maxlklaxl/python-tsl2591/blob/master/tsl2591/read_tsl.py


This code is basically an adaptation of the Arduino_TSL2591 library from
adafruit: https://github.com/adafruit/Adafruit_TSL2591_Library

for configuring I2C in a raspberry
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

datasheet:
http://ams.com/eng/Products/Light-Sensors/Light-to-Digital-Sensors/TSL25911

'''
import time
import logging

log = logging.getLogger(__name__)

VISIBLE = 2  # channel 0 - channel 1
INFRARED = 1  # channel 1
FULLSPECTRUM = 0  # channel 0

ADDR = 0x29
READBIT = 0x01
COMMAND_BIT = 0xA0  # bits 7 and 5 for 'command normal'
CLEAR_BIT = 0x40  # Clears any pending interrupt (write 1 to clear)
WORD_BIT = 0x20  # 1 = read/write word (rather than byte)
BLOCK_BIT = 0x10  # 1 = using block read/write
ENABLE_POWERON = 0x01
ENABLE_POWEROFF = 0x00
ENABLE_AEN = 0x02
ENABLE_AIEN = 0x10
CONTROL_RESET = 0x80
LUX_DF = 408.0
LUX_COEFB = 1.64  # CH0 coefficient
LUX_COEFC = 0.59  # CH1 coefficient A
LUX_COEFD = 0.86  # CH2 coefficient B

REGISTER_ENABLE = 0x00
REGISTER_CONTROL = 0x01
REGISTER_THRESHHOLDL_LOW = 0x02
REGISTER_THRESHHOLDL_HIGH = 0x03
REGISTER_THRESHHOLDH_LOW = 0x04
REGISTER_THRESHHOLDH_HIGH = 0x05
REGISTER_INTERRUPT = 0x06
REGISTER_CRC = 0x08
REGISTER_ID = 0x0A
REGISTER_CHAN0_LOW = 0x14
REGISTER_CHAN0_HIGH = 0x15
REGISTER_CHAN1_LOW = 0x16
REGISTER_CHAN1_HIGH = 0x17
INTEGRATIONTIME_100MS = 0x00
INTEGRATIONTIME_200MS = 0x01
INTEGRATIONTIME_300MS = 0x02
INTEGRATIONTIME_400MS = 0x03
INTEGRATIONTIME_500MS = 0x04
INTEGRATIONTIME_600MS = 0x05

GAIN_LOW = 0x00  # low gain (1x)
GAIN_MED = 0x10  # medium gain (25x)
GAIN_HIGH = 0x20  # medium gain (428x)
GAIN_MAX = 0x30  # max gain (9876x)

INTEGRATIONTIME_TO_MS = {
    INTEGRATIONTIME_100MS: 100,
    INTEGRATIONTIME_200MS: 200,
    INTEGRATIONTIME_300MS: 300,
    INTEGRATIONTIME_400MS: 400,
    INTEGRATIONTIME_500MS: 500,
    INTEGRATIONTIME_600MS: 600,
}

GAIN_TO_VALUE = {
    GAIN_LOW: 1,
    GAIN_MED: 25,
    GAIN_HIGH: 428,
    GAIN_MAX: 9876,
}


class Tsl2591(object):
    def __init__(self, bus, sensor_address=0x29):
        self._bus = bus
        self._i2c_address = sensor_address

        self._integration_time = INTEGRATIONTIME_100MS
        self._gain = GAIN_MED
        self.set_timing(self._integration_time)
        self.set_gain(self._gain)
        self._disable()

    def set_timing(self, integration):
        self._integration_time = integration
        self._write_control(self._integration_time | self._gain)

    def set_gain(self, gain):
        self._gain = gain
        self._write_control(self._integration_time | self._gain)

    def get_gain(self):
        return self._gain

    def calculate_lux(self, ch0, ch1):
        if ch0 == 0xFFFF or ch1 == 0xFFFF:  # overflow?
            log.error("overflow!")
            return 10000  # Some big value is less wrong than zero

        log.info("ch0=%s ch1=%s", ch0, ch1)

        integration_time = INTEGRATIONTIME_TO_MS.get(self._integration_time, 100)
        gain = GAIN_TO_VALUE.get(self._gain, 1)
        log.info("integration_time=%s gain=%s", integration_time, gain)

        cpl = float(integration_time) * float(gain) / LUX_DF
        log.info("cpl=%s", cpl)

        # lux1 = (full - (LUX_COEFB * ir)) / cpl
        # lux2 = ((LUX_COEFC * full) - (LUX_COEFD * ir)) / cpl
        # The highest value is the approximate lux equivalent
        # lux = max([lux1, lux2])

        # lux = ( ((float)ch0 - (float)ch1 )) * (1.0F - ((float)ch1/(float)ch0) ) / cpl;
        ch0, ch1 = float(ch0), float(ch1)
        lux = (ch0 - ch1) * (1.0 - (ch1 / ch0)) / cpl
        return lux

    def get_full_luminosity(self):
        self._enable()
        time.sleep(0.120*self._integration_time+1)  # not sure if we need it "// Wait x ms for ADC to complete"
        ch0 = self._bus.read_word_data(self._i2c_address, COMMAND_BIT | REGISTER_CHAN0_LOW)
        ch1 = self._bus.read_word_data(self._i2c_address, COMMAND_BIT | REGISTER_CHAN1_LOW)
        self._disable()
        return ch0, ch1

    def measure_lux(self):
        ch0, ch1 = self.get_full_luminosity()
        return self.calculate_lux(ch0, ch1)

    def _enable(self):
        self._bus.write_byte_data(self._i2c_address, COMMAND_BIT | REGISTER_ENABLE,
            ENABLE_POWERON | ENABLE_AEN | ENABLE_AIEN)

    def _disable(self):
        self._bus.write_byte_data(self._i2c_address, COMMAND_BIT | REGISTER_ENABLE,
            ENABLE_POWEROFF)

    def _write_control(self, value):
        self._enable()
        self._bus.write_byte_data(self._i2c_address, COMMAND_BIT | REGISTER_CONTROL, value)
        self._disable()

    # def get_luminosity(self, channel):
    #     ch0, ch1 = self.get_full_luminosity()
    #     if channel == FULLSPECTRUM:
    #         return ch0
    #     elif channel == INFRARED:
    #         return ch1
    #     elif channel == VISIBLE:
    #         return ch0 - ch1
    #     return 0


# if __name__ == '__main__':

#     tsl = Tsl2591()  # initialize
#     full, ir = tsl.get_full_luminosity()  # read raw values (full spectrum and ir spectrum)
#     lux = tsl.calculate_lux(full, ir)  # convert raw values to lux
#     print (lux, full, ir)
#     print ()

#     def test(int_time=INTEGRATIONTIME_100MS, gain=GAIN_LOW):
#         tsl.set_gain(gain)
#         tsl.set_timing(int_time)
#         full_test, ir_test = tsl.get_full_luminosity()
#         lux_test = tsl.calculate_lux(full_test, ir_test)
#         print ('Lux = %f  full = %i  ir = %i' % (lux_test, full_test, ir_test))
#         print("integration time = %i" % tsl.get_timing())
#         print("gain = %i \n" % tsl.get_gain())

#     for i in [INTEGRATIONTIME_100MS,
#               INTEGRATIONTIME_200MS,
#               INTEGRATIONTIME_300MS,
#               INTEGRATIONTIME_400MS,
#               INTEGRATIONTIME_500MS,
#               INTEGRATIONTIME_600MS]:
#         test(i, GAIN_LOW)

#     for i in [GAIN_LOW,
#               GAIN_MED,
#               GAIN_HIGH,
#               GAIN_MAX]:
#         test(INTEGRATIONTIME_100MS, i)
