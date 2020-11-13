from typing import List, Union

from django.db.models import Q, QuerySet

from kaffepause.friendships.enums import (
    BaseFriendshipStatusEnum,
    DefaultFriendshipStatus,
    NonFriendsFriendshipStatus,
)
from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.users.models import User


def get_friends(user: User) -> Union[QuerySet, List[User]]:
    return get_friendships_for(user, FriendshipStatus.objects.friends())


def get_incoming_requests(user: User) -> Union[QuerySet, List[User]]:
    return get_incoming_friendships_for(user, FriendshipStatus.objects.requested())


def get_outgoing_requests(user: User) -> Union[QuerySet, List[User]]:
    return get_outgoing_friendships_for(user, FriendshipStatus.objects.requested())


def get_outgoing_blocks(user: User) -> Union[QuerySet, List[User]]:
    return get_outgoing_friendships_for(user, FriendshipStatus.objects.blocked())


def get_incoming_blocks(user: User) -> Union[QuerySet, List[User]]:
    return get_incoming_friendships_for(user, FriendshipStatus.objects.blocked())


def get_friendships_for(
    user: User, status: FriendshipStatus, symmetrical: bool = True
) -> Union[QuerySet, List[User]]:
    """
    Returns a QuerySet of user objects with which the given user has
    established a friendship.
    """

    query = _get_incoming_query(user, status)

    if symmetrical:
        query |= _get_outgoing_query(user, status)

    return User.objects.filter(query)


def get_incoming_friendships_for(
    user: User, status: FriendshipStatus
) -> Union[QuerySet, List[User]]:
    """
    Returns a QuerySet of user objects which have created a friendship to
    the given user. to_user = user, from_user = other_user
    """
    return User.objects.filter(_get_incoming_query(user, status))


def get_outgoing_friendships_for(
    user: User, status: FriendshipStatus
) -> Union[QuerySet, List[User]]:
    """Returns a QuerySet of user objects which the given user has created a friendship to."""
    return User.objects.filter(_get_outgoing_query(user, status))


def _get_incoming_query(user, status):
    return Q(from_users__to_user=user, from_users__status=status)


def _get_outgoing_query(user, status):
    return Q(to_users__from_user=user, to_users__status=status)


def friendship_exists(from_user, to_user, status=None, symmetrical=False):
    """
    Returns boolean whether or not a friendship exists between the given
    users.  An optional :class:`FriendshipStatus` instance can be specified.

    If symmetrical = True the reversed friendship existence is also queried for.
    """

    query = Q(from_user=from_user, to_user=to_user)

    if status:
        query &= Q(status=status)

    if symmetrical:
        query |= Q(from_user=to_user, to_user=from_user)

        if status:
            query &= Q(status=status)

    return Friendship.objects.filter(query).exists()


def get_single_friendship(from_user, to_user, status=None):
    """
    Returns the friendship object between the given users.
    An optional :class:`FriendshipStatus` instance can be specified.
    """

    query = Q(from_user=from_user, to_user=to_user) | Q(
        from_user=to_user, to_user=from_user
    )

    if status:
        query &= Q(status=status)

    friendships = Friendship.objects.filter(query).first()

    if not friendships:
        raise Friendship.DoesNotExist

    return friendships


def get_single_incoming_friendship(
    actor: User, from_user: User, status: FriendshipStatus
):
    """Returns the incoming friendship object, if found."""
    return Friendship.objects.filter(from_user=from_user, to_user=actor, status=status)


def get_single_outgoing_friendship(
    actor: User, to_user: User, status: FriendshipStatus
):
    """Returns the outgoing friendship object, if found."""
    return Friendship.objects.filter(from_user=actor, to_user=to_user, status=status)


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
    actor, user
) -> DefaultFriendshipStatus:
    """Returns the friendship status for the given users."""
    friendship = get_single_friendship(actor, user)
    status = DefaultFriendshipStatus.from_name(friendship.status.name)
    return status.name
