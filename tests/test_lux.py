import pytest

from cocorico.lux import Lux


@pytest.fixture(scope='module')
def lux():
    lux = Lux()
    yield lux
    lux.close()


def test_api(lux):
    assert lux.is_dark is True
    assert lux.is_lighted is False
    assert str(lux)


def test_threshold(lux, mocker):
    mocker.patch.object(lux, '_sensor')

    lux._sensor.measure_lux.return_value = 2
    lux._poll()
    assert lux.is_dark is False
    assert lux.is_lighted is False

    lux._sensor.measure_lux.return_value = 10
    lux._poll()
    assert lux.is_dark is False
    assert lux.is_lighted is True
