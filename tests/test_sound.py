import pytest

from cocorico.sound import Sound
from cocorico.hal.gpio import GPIO




@pytest.fixture
def s():
    sound = Sound()
    yield sound
    sound.close()


def test_just_api_calls(s, m_pyaudio):
    s.stop()
    s.play_startup()
    s.refresh()
    s.set_alarm()
    s.stop()
    s.refresh()
    s.stop()
    s.close()


def test_engine(s, mocker, m_pyaudio):
    s.play_startup()

    assert m_pyaudio.open.called

    stream = m_pyaudio.open.return_value
    assert stream.start_stream.called

    s.stop()
    assert stream.stop_stream.called
    assert stream.close.called

    m_pyaudio.reset_mock()
    s.stop()
    assert not stream.stop_stream.called


def test_amplifier(s):
    assert GPIO._outputs_values[4] == GPIO.HIGH

    s.play_startup()
    assert GPIO._outputs_values[4] == GPIO.LOW

    s.stop()
    assert GPIO._outputs_values[4] == GPIO.HIGH


def test_close(s, mocker, m_pyaudio):
    s.play_startup()

    m_pyaudio.reset_mock()

    s.close()

    m_stream = mocker.call.open()
    expected = [m_stream.stop_stream(), m_stream.close(), mocker.call.terminate()]
    assert m_pyaudio.mock_calls == expected
