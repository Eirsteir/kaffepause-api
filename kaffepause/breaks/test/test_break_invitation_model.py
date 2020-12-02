from datetime import timedelta
from unittest.mock import PropertyMock, patch

import pytest
from django.utils import timezone

from kaffepause.breaks.exceptions import (
    AlreadyReplied,
    InvitationExpired,
    InvitationNotAddressedAtUser,
)
from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("expires_in_hours, expected", [(-1, True), (1, False)])
def test_is_expired(expires_in_hours, expected):
    """Should return whether the invitation has expired."""
    now = timezone.now()
    expiry = now + timedelta(hours=expires_in_hours)

    invitation = BreakInvitationFactory()
    invitation.subject.connect(BreakFactory(start_time=expiry))

    assert invitation.is_expired == expected


@patch("kaffepause.breaks.models.BreakInvitation.is_expired", new_callable=PropertyMock)
def test_check_expiry_when_expired_raises_exception(mock_is_expired):
    """Should raise an exception if the invitation has expired."""
    mock_is_expired.return_value = True
    invitation = BreakInvitationFactory.build()

    with pytest.raises(InvitationExpired):
        invitation._check_expiry()


def test_assert_is_addressed_at_user_when_is_not_addressed_at_user_raises_exception():
    """Should raise an exception if the invitation is not addressed at the user."""
    invitation = BreakInvitationFactory()
    user = UserFactory()

    with pytest.raises(InvitationNotAddressedAtUser):
        invitation._assert_is_addressed_at_user(user)


def test_assert_user_has_not_replied_when_user_has_accepted_raises_exception():
    """Should raise an exception if the user has already accepted the invitation."""
    invitation = BreakInvitationFactory()
    user = UserFactory()
    invitation.acceptees.connect(user)

    with pytest.raises(AlreadyReplied):
        invitation._assert_user_have_not_replied(user)


def test_assert_user_has_not_replied_when_user_has_declined_raises_exception():
    """Should raise an exception if the user has already declined the invitation."""
    invitation = BreakInvitationFactory()
    user = UserFactory()
    invitation.declinees.connect(user)

    with pytest.raises(AlreadyReplied):
        invitation._assert_user_have_not_replied(user)
