from cocorico.app import App


def test_first_cycle():
    app = App()
    app.initialize()
    app.close()


def test_cycle(previous, now):
    app = App()
    app.routine(previous, now)
    app.routine(previous, now)
    app.close()


def test_actions():
    app = App()
    app.action_up()
    app.action_down()
    app.action_onoff()
    app.action_stop()
    app.action_snooze()
    app.refresh()
    app.close()


def test_alarm():
    app = App()
    app.state.set_alarm(progression=0.1)
    app.refresh()

    app.state.set_alarm(progression=0.9)
    app.refresh()

    app.action_snooze()
    app.close()
