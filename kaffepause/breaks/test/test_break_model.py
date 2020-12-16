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

    break_ = Break(starting_at=start_time).save()

    assert break_.starting_at == start_time


def test_create_with_start_time_in_the_past_fails():
    """It should not be possible to create a break starting in the past."""
    now = timezone.now()
    start_time = now + timedelta(hours=-1)

    with pytest.raises(InvalidBreakStartTime):
        Break(starting_at=start_time).save()
