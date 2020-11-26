import pytest

from kaffepause.accounts.test.factories import AccountFactory
from kaffepause.breaks.enums import InvitationReply
from kaffepause.breaks.exceptions import InvalidInvitationUpdate
from kaffepause.breaks.models import BreakInvitation
from kaffepause.breaks.services import (
    __reply_to_invitation,
    accept_break_invitation,
    create_and_invite_friends_to_a_break,
    decline_break_invitation,
    ignore_break_invitation,
)
from kaffepause.breaks.test.factories import BreakInvitationFactory
from kaffepause.common.utils import three_hours_from_now
from kaffepause.friendships.test.factories import FriendshipFactory

pytestmark = pytest.mark.django_db


def test_create_and_invite_friends_to_a_break_invites_all_friends_to_break(
    user, are_friends_status, requested_status
):
    """Creating a break should invite all the users friends to that break."""
    amount_of_friends = 6
    amount_of_friends_half = int(amount_of_friends / 2)

    FriendshipFactory.create_batch(
        amount_of_friends_half, from_user=user, status=are_friends_status
    )
    FriendshipFactory.create_batch(
        amount_of_friends_half, to_user=user, status=are_friends_status
    )

    requesting_friend = AccountFactory()
    FriendshipFactory(
        from_user=requesting_friend, to_user=user, status=requested_status
    )

    created_break = create_and_invite_friends_to_a_break(actor=user)

    invitations = BreakInvitation.objects.filter(subject=created_break)

    assert invitations.count() == amount_of_friends
    assert not invitations.filter(recipient_id=requesting_friend.id).exists()


def test_create_and_invite_friends_to_a_break_adds_actor_to_participants(user):
    """Creating a break should add the actor to the list of participants for that break."""
    created_break = create_and_invite_friends_to_a_break(actor=user)

    assert created_break.participants.count() == 1
    assert created_break.participants.filter(id=user.id).exists()


def test_create_and_invite_friends_to_a_break_with_start_time_sets_start_time(user):
    """Creating a break with start time should set the start time to the given time."""
    start_time = three_hours_from_now()

    created_break = create_and_invite_friends_to_a_break(
        actor=user, start_time=start_time
    )

    assert created_break.start_time == start_time


def test_reply_to_invitation(user):
    """Should update the invitation reply to given reply action"""
    invitation = BreakInvitationFactory(recipient=user, reply=None)
    invitation = __reply_to_invitation(
        actor=user, invitation=invitation, action=invitation.accept
    )

    assert invitation.reply == InvitationReply.ACCEPTED


def test_reply_to_invitation_when_invitation_does_not_belong_to_the_actor(user):
    """Only the recipient of an invitation should be able to reply to it."""
    invitation = BreakInvitationFactory(reply=None)

    with pytest.raises(InvalidInvitationUpdate):
        __reply_to_invitation(
            actor=user, invitation=invitation, action=invitation.accept
        )


@pytest.mark.parametrize(
    "reply_action, expected_reply",
    [
        (accept_break_invitation, InvitationReply.ACCEPTED),
        (decline_break_invitation, InvitationReply.DECLINED),
        (ignore_break_invitation, InvitationReply.IGNORED),
    ],
)
def test_replying_to_break_invitation(user, reply_action, expected_reply):
    """Should update the invitation reply to given reply."""
    invitation = BreakInvitationFactory(recipient=user, reply=None)

    invitation = reply_action(actor=user, invitation=invitation)

    assert invitation.reply == expected_reply
