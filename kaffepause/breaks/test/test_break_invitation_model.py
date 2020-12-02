from datetime import timedelta

import pytest
from django.utils import timezone

from kaffepause.breaks.enums import InvitationReply
from kaffepause.breaks.exceptions import (
    AlreadyReplied,
    InvalidInvitationExpiration,
    InvitationExpired,
)
from kaffepause.breaks.test.factories import BreakInvitationFactory

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("expires_in_hours, expected", [(-1, True), (1, False)])
def test_is_expired(expires_in_hours, expected):
    """Should return whether the invitation has expired."""
    now = timezone.now()
    expiry = now + timedelta(hours=expires_in_hours)

    invitation = BreakInvitationFactory.build(expiry=expiry)

    assert invitation.is_expired == expected


def test_save_with_invalid_expiry():
    """It should not be possible to set expiration in the past."""
    now = timezone.now()
    expiry = now + timedelta(hours=-1)

    with pytest.raises(InvalidInvitationExpiration):
        BreakInvitationFactory(expiry=expiry)


def test_accept():
    """Should update the invitation reply to accepted and add the recipient to break participants."""
    invitation = BreakInvitationFactory(reply=None)
    invitation.accept()

    recipient = invitation.recipient

    assert invitation.reply == InvitationReply.ACCEPTED
    assert invitation.subject.participants.filter(id=recipient.id).exists()


def test_decline():
    """Should update the invitation reply to declined."""
    invitation = BreakInvitationFactory(reply=None)

    invitation.decline()

    assert invitation.reply == InvitationReply.DECLINED


def test_ignore():
    """Should update the invitation reply to ignored."""
    invitation = BreakInvitationFactory(reply=None)

    invitation.ignore()

    assert invitation.reply == InvitationReply.IGNORED
