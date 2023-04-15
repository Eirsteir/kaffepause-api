from unittest.mock import PropertyMock, patch

import pytest

from kaffepause.breaks.exceptions import (
    AlreadyReplied,
    InvitationExpired,
    InvitationNotAddressedAtUser,
)
from kaffepause.breaks.test.factories import BreakInvitationFactory
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


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
    invitation.confirmed.connect(user)

    with pytest.raises(AlreadyReplied):
        invitation._assert_user_have_not_replied(user)


def test_assert_user_has_not_replied_when_user_has_declined_raises_exception():
    """Should raise an exception if the user has already declined the invitation."""
    invitation = BreakInvitationFactory()
    user = UserFactory()
    invitation.decliners.connect(user)

    with pytest.raises(AlreadyReplied):
        invitation._assert_user_have_not_replied(user)
