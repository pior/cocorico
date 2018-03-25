from cocorico.sound import Sound


def test_just_api_calls(mocker):
    m_engine = mocker.patch('cocorico.sound.Engine')

    s = Sound()

    s.stop()
    s.play_startup()
    s.refresh()
    s.play_alarm()
    s.play_alarm()
    s.stop()
    s.refresh()
    s.stop()
    s.close()


def test_play(mocker):
    m_engine_class = mocker.patch('cocorico.sound.Engine')

    s = Sound()
    m_engine_class.assert_called_once_with()
    m_engine = m_engine_class.return_value

    s.play_startup()
    assert m_engine.start.called

    s.stop()
    assert m_engine.stop.called


def test_close(mocker):
    m_pyaudio = mocker.patch('cocorico.sound.engine.pyaudio')

    s = Sound()
    s.play_startup()

    m_pyaudio.reset_mock()

    s.close()

    assert m_pyaudio.mock_calls == [mocker.call.PyAudio().terminate()]
