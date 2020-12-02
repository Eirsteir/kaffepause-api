import pytest

from kaffepause.breaks.services import create_break_and_invitations
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_break_and_invitations_creates_break_and_invites_addressees_which_are_following_the_actor():
    """When a break is created, only the friends following the actor should be invited."""
    actor = UserFactory()
    friends = UserFactory.create_batch(10)
    for friend in friends:
        actor.add_friend(friend)

    other_user = UserFactory()
    addressee_ids = list(map(lambda friend: friend.uid, friends))
    addressee_ids.append(other_user.uid)

    create_break_and_invitations(actor, addressee_ids)

    break_invitation = actor.sent_break_invitations.all()[0]

    invited_users = break_invitation.addressees.filter(uid__in=addressee_ids)
    assert len(invited_users) == len(friends)
    assert other_user not in break_invitation.addressees


def test_create_and_invite_followers_to_a_break_creates_break_and_invites_all_the_actors_followers():
    """When a break is created without specifying addressees, all of the actors followers should be invited."""
    pass


def _create_break_and_invitation_creates_break_and_invitation():
    """Should create a break and corresponding invitation."""
    pass


def test_create_break_creates_break_with_correct_connections():
    """Creating a break should connect the actor to its participants."""
    pass


def test_create_invitation_creates_invitation_with_correct_connections():
    """Creating an invitation should connect the actor as sender, the break as subject and addressees as such."""
    pass
