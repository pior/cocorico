import datetime

import pytest

from cocorico.clock import Clock


@pytest.fixture(params=[{}, {'hour': 1}, {'hour': 12}, {'hour': 23}])
def now(request):
    return Clock().with_values(**request.param)


@pytest.fixture
def previous(now):
    return now - datetime.timedelta(seconds=1)
