from datetime import timedelta

import pytest
from django.utils import timezone

from kaffepause.breaks.exceptions import InvalidBreakStartTime
from kaffepause.breaks.models import Break
from kaffepause.common.utils import time_from_now

pytestmark = pytest.mark.django_db


def test_create_with_start_time_in_the_future_creates_break():
    """It should only be possible to create a break starting in the future."""
    start_time = time_from_now(hours=1)

    break_ = Break(start_time=start_time).save()

    assert break_.start_time == start_time


def test_create_with_start_time_in_the_past_raises_exception():
    """It should not be possible to create a break starting in the past."""
    now = timezone.now()
    start_time = now + timedelta(hours=-1)

    with pytest.raises(InvalidBreakStartTime):
        Break(start_time=start_time).save()
