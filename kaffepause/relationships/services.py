from typing import Any

from django.utils.translation import gettext_lazy as _
from neomodel import db

from kaffepause.relationships.exceptions import (
    CannotAcceptFriendRequest,
    InvalidFriendshipDeletion,
    RelationshipAlreadyExists,
)
from kaffepause.relationships.models import FriendRel
from kaffepause.users.models import User


def send_friend_request(actor: User, to_user: User) -> FriendRel:
    """Connect two users with a requested friendship connection."""
    if relationship_exists(actor, to_user):
        raise RelationshipAlreadyExists()

    return actor.send_friend_request(to_user)


def cancel_friend_request(actor: User, to_user: User):
    return actor.cancel_friend_request(to_user)


def relationship_exists(user, other):
    query = """
    MATCH (user:User)-[:ARE_FRIENDS| :REQUESTED_TO_FRIEND | :REQUESTED_FROM_FRIEND | :BLOCKED]-(other:User)
    WHERE user.uid = {user_uid} AND other.uid = {other_uid}
    RETURN other
    """
    params = dict(user_uid=user.uid, other_uid=other.uid)
    results, meta = db.cypher_query(query, params)
    people = [User.inflate(row[0]) for row in results]
    return people


def accept_friend_request(actor: User, requester: User) -> FriendRel:
    """
    Create a friendship relationship between given nodes.
    The requester must first have sent a friend request.
    """
    # TODO: fix semantics

    existing_friendship = actor.friends.relationship(requester)
    if existing_friendship:
        return existing_friendship

    can_accept_friend_request = actor.incoming_friend_requests.relationship(requester)
    if can_accept_friend_request:
        return requester.add_friend(actor)

    raise CannotAcceptFriendRequest


def delete_friendship(actor: User, user: User):
    """
    Deletes a friendship from one user to another, following some simple rules.

    - Both users should be able to delete a requested friendship
    - Both users should be able to delete an accepted friendship
    - Only the one blocking should be able to delete a blocked friendship
    """

    raise NotImplementedError()


def _attempt_to_delete_blocked_friendship(actor: User, friendship):
    """
    Assures only the one blocking can delete the friendship.

    :raises :class:`InvalidFriendshipDeletion` if the friendship status is not blocked
        or if the one being blocked is acting.
    """
    if not friendship.is_blocked:
        raise InvalidFriendshipDeletion(
            _("Cannot delete a blocked friendship when the friendship is not blocked")
        )

    if actor == friendship.from_user:
        return friendship.delete()

    raise InvalidFriendshipDeletion(
        _("Only the blocking to_user can delete this friendship")
    )


def deny_blocked_relationship(user: User, other: User):
    raise NotImplementedError
