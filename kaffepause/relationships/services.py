from neomodel import db

from kaffepause.relationships.exceptions import (
    CannotAcceptFriendRequest,
    CannotRejectFriendRequest,
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


def remove_friend(actor: User, friend: User):
    return actor.remove_friend(friend)


def deny_blocked_relationship(user: User, other: User):
    raise NotImplementedError
