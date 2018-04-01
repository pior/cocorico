import time

from cocorico.state import State


def test_init():
    state = State()
    st, pr = state.get()
    assert st == state.STANDBY
    assert pr == 1


def test_alarm():
    state = State()

    state.set_alarm(0.5)
    st, pr = state.get()
    assert st == state.ALARM
    assert pr == 0.5
    assert state.is_alarm()

    state.set_standby()
    st, pr = state.get()
    assert st == state.STANDBY
    assert pr == 1
    assert not state.is_alarm()


def test_state_timeout():
    state = State()

    state.set_alarm_time()

    assert state.get() == (state.ALARM_TIME, 1)

    time.sleep(2.1)
    assert state.get() == (state.STANDBY, 1)
