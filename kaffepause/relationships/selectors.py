from typing import Iterable

from django.db.models import Q

from kaffepause.relationships.enums import (
    BaseFriendshipStatusEnum,
    DefaultFriendshipStatus,
    NonFriendsFriendshipStatus,
)
from kaffepause.users.models import User


def get_friends(user: User) -> Iterable[User]:
    return user.friends.all()


def get_incoming_requests(
    user: User,
) -> Iterable[User]:
    return user.incoming_friend_requests.all()


def get_outgoing_requests(
    user: User,
) -> Iterable[User]:
    return user.outgoing_friend_requests.all()


def get_outgoing_blocks(
    user: User,
) -> Iterable[User]:
    raise NotImplementedError()


def get_incoming_blocks(
    user: User,
) -> Iterable[User]:
    raise NotImplementedError()


def friendship_exists(from_user, to_user, status=None, symmetrical=False):
    """
    Returns boolean whether or not a friendship exists between the given
    users.  An optional :class:`FriendshipStatus` instance can be specified.

    If symmetrical = True the reversed friendship existence is also queried for.
    """
    raise NotImplementedError()


def get_single_incoming_friendship(
    actor: User,
    from_user: User,
):
    """Returns the incoming friendship object, if found."""
    raise NotImplementedError()


def get_single_outgoing_friendship(
    actor: User,
    to_user: User,
):
    """Returns the outgoing friendship object, if found."""
    raise NotImplementedError()


def get_friendship_status(actor: User, user: User) -> BaseFriendshipStatusEnum:
    """
    Returns the friendship status as viewed by the user when
    only the users are available in the current context.
    If no such friendship exists, a default value of 'CAN_REQUEST' is returned.
    """
    if friendship_exists(actor, user):
        return _get_friendship_status_for_existing_friendship(actor, user)

    return NonFriendsFriendshipStatus.CAN_REQUEST


# TODO: might throw exception
def _get_friendship_status_for_existing_friendship(
    actor: User, user: User
) -> DefaultFriendshipStatus:
    """Returns the friendship status for the given users."""
    raise NotImplementedError()


def get_mutual_friends(actor: User, user: User) -> Iterable[User]:
    """Returns the mutual friends for the given users."""
    raise NotImplementedError()