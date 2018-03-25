from cocorico.app import App


def test_first_cycle(now):
    app = App()
    app.routine(None, now)
    app.close()


def test_cycle(previous, now):
    app = App()
    app.routine(previous, now)
    app.close()
