import pytest

from cocorico.button import Button
from cocorico.hal.gpio import GPIO

PIN_NUM = 7


@pytest.mark.parametrize('bounce_inputs', [
    (True, [GPIO.HIGH]),
    (True, [GPIO.LOW] * 9 + [GPIO.HIGH]),
    (True, [GPIO.LOW] * 4 + [GPIO.HIGH] + [GPIO.LOW] * 5),
    (False, [GPIO.LOW] * 10),
])
def test_debouncing(mocker, bounce_inputs):
    bounce, inputs = bounce_inputs

    GPIO._mock_set_input_values(PIN_NUM, inputs)

    callback = mocker.Mock()

    b = Button(PIN_NUM, callback)
    b._gpio_callback(PIN_NUM)

    if bounce:
        assert not callback.called
    else:
        assert callback.called
