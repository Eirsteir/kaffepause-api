import pytest

pytestmark = pytest.mark.django_db


def test_create_break_and_invitations_creates_break_and_invites_addressees_which_are_following_the_actor():
    """When a break is created, only the users following the actor should be invited."""
    pass


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
