from datetime import timedelta

import pytest
from django.utils import timezone

from kaffepause.breaks.exceptions import InvalidInvitationExpiration
from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("expires_in_hours, expected", [(-1, True), (1, False)])
def test_is_expired(expires_in_hours, expected):
    """Should return whether the invitation has expired."""
    now = timezone.now()
    expiry = now + timedelta(hours=expires_in_hours)

    invitation = BreakInvitationFactory()
    invitation.subject.connect(BreakFactory(start_time=expiry))
    assert invitation.is_expired == expected


def test_accept():
    """Should update the invitation reply to accepted and add the recipient to break participants."""
    pass


def test_decline():
    """Should update the invitation reply to declined."""
    pass
