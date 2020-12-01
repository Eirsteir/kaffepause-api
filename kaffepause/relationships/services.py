from kaffepause.relationships.exceptions import (
    CannotAcceptFriendRequest,
    CannotRejectFriendRequest,
    RelationshipAlreadyExists,
)
from kaffepause.relationships.models import FriendRel
from kaffepause.relationships.selectors import relationship_exists
from kaffepause.users.models import User


def send_friend_request(actor: User, to_user: User) -> FriendRel:
    """Connect two users with a requested friendship connection."""
    if relationship_exists(actor, to_user):
        raise RelationshipAlreadyExists

    return actor.send_friend_request(to_user)


def cancel_friend_request(actor: User, to_user: User):
    return actor.cancel_friend_request(to_user)


def accept_friend_request(actor: User, requester: User) -> FriendRel:
    """
    Create a friendship relationship between given nodes.
    The requester must first have sent a friend request.
    """
    # TODO: fix semantics

    existing_friendship = actor.friends.relationship(requester)
    if existing_friendship:
        return existing_friendship

    if can_reply_to_friend_request(actor, requester):
        return requester.add_friend(actor)

    raise CannotAcceptFriendRequest


def reject_friend_request(actor: User, requester: User) -> User:
    if can_reply_to_friend_request(actor, requester):
        return actor.reject_friend_request(requester)

    raise CannotRejectFriendRequest


def can_reply_to_friend_request(actor, requester):
    """The actor can only reply to a friend request if the requester has sent one."""
    return actor.incoming_friend_requests.relationship(requester)


def unfriend_user(actor: User, friend: User):
    return actor.remove_friend(friend)
