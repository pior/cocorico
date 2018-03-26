import datetime

import pytest

from cocorico.clock import Clock


@pytest.fixture(params=[{}, {'hour': 1}, {'hour': 12}, {'hour': 23}])
def now(request):
    return Clock().with_values(**request.param)


@pytest.fixture
def previous(now):
    return now - datetime.timedelta(seconds=1)


@pytest.fixture(autouse=True)
def m_pyaudio(mocker):
    m = mocker.patch('cocorico.sound.engine.pyaudio')
    pa = m.PyAudio.return_value
    pa.get_device_count.return_value = 1
    pa.get_device_info_by_index.return_value = {
        'index': 0,
        'name': 'TESTDEVICE',
        'maxOutputChannels': 2,
    }
    return pa
