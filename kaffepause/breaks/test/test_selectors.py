from datetime import datetime, timedelta

import pytest
import pytz

from kaffepause.breaks.selectors import get_break_invitations_awaiting_reply
from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory

pytestmark = pytest.mark.django_db


def test_get_break_invitations_awaiting_reply_returns_unanswered_invitations(user):
    """Should return all non-expired break invitations the user has not replied to."""
    unanswered_break_invitation = BreakInvitationFactory()
    unanswered_break_invitation.subject.connect(BreakFactory())
    unanswered_break_invitation.addressees.connect(user)

    an_hour_ago = datetime.now(pytz.utc) - timedelta(hours=10)
    expired_break = BreakFactory()
    expired_break.start_time = an_hour_ago
    expired_break.save()
    expired_break_invitation = BreakInvitationFactory()
    expired_break_invitation.subject.connect(expired_break)
    expired_break_invitation.addressees.connect(user)

    accepted_break_invitation = BreakInvitationFactory()
    accepted_break_invitation.subject.connect(BreakFactory())
    accepted_break_invitation.addressees.connect(user)
    accepted_break_invitation.acceptees.connect(user)

    declined_break_invitation = BreakInvitationFactory()
    declined_break_invitation.subject.connect(BreakFactory())
    declined_break_invitation.addressees.connect(user)
    declined_break_invitation.declinees.connect(user)

    actual_break_invitations = get_break_invitations_awaiting_reply(actor=user)

    assert unanswered_break_invitation in actual_break_invitations
    assert expired_break_invitation not in actual_break_invitations
    assert accepted_break_invitation not in actual_break_invitations
    assert declined_break_invitation not in actual_break_invitations


def test_get_break_invitations_awaiting_reply_returns_unanswered_invitations_expired_five_minutes_ago(
    user,
):
    """Should return unanswered invitations who's break has started within 5 minutes ago."""
    two_minutes_ago = datetime.now(pytz.utc) - timedelta(minutes=2)
    non_expired_break = BreakFactory()
    non_expired_break.start_time = two_minutes_ago
    non_expired_break.save()
    non_expired_break_invitation = BreakInvitationFactory()
    non_expired_break_invitation.subject.connect(non_expired_break)
    non_expired_break_invitation.addressees.connect(user)

    ten_minutes_ago = datetime.now(pytz.utc) - timedelta(minutes=10)
    expired_break = BreakFactory()
    expired_break.start_time = ten_minutes_ago
    expired_break.save()
    expired_break_invitation = BreakInvitationFactory()
    expired_break_invitation.subject.connect(expired_break)
    expired_break_invitation.addressees.connect(user)

    actual_break_invitations = get_break_invitations_awaiting_reply(actor=user)

    assert non_expired_break_invitation in actual_break_invitations
    assert expired_break_invitation not in actual_break_invitations
