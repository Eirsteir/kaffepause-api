from typing import Iterable, List

from neomodel import db

from kaffepause.relationships.enums import (
    BaseFriendshipStatusEnum,
    DefaultFriendshipStatus,
    NonFriendsFriendshipStatus,
)
from kaffepause.users.models import User


def get_friends(user: User) -> List[User]:
    return user.friends.all()


def get_incoming_requests(
    user: User,
) -> List[User]:
    return user.incoming_friend_requests.all()


def get_outgoing_requests(
    user: User,
) -> List[User]:
    return user.outgoing_friend_requests.all()


def get_outgoing_blocks(
    user: User,
) -> List[User]:
    return user.blocking.all()


def get_incoming_blocks(
    user: User,
) -> List[User]:
    raise NotImplementedError()


def relationship_exists(user, other):
    """Returns boolean whether or not a relationship of any kind exists between the given users."""
    query = """
    MATCH (user:User)-[:ARE_FRIENDS| :REQUESTED_TO_FRIEND | :REQUESTED_FROM_FRIEND | :BLOCKED]-(other:User)
    WHERE user.uid = {user_uid} AND other.uid = {other_uid}
    RETURN other
    """
    params = dict(user_uid=user.uid, other_uid=other.uid)
    results, meta = db.cypher_query(query, params)
    people = [User.inflate(row[0]) for row in results]
    return people


def get_friendship_status(actor: User, user: User) -> BaseFriendshipStatusEnum:
    """
    Returns the friendship status as viewed by the user when
    only the users are available in the current context.
    If no such friendship exists, a default value of 'CAN_REQUEST' is returned.
    """
    if relationship_exists(actor, user):
        return _get_friendship_status_for_existing_friendship(actor, user)

    return NonFriendsFriendshipStatus.CAN_REQUEST


def _get_friendship_status_for_existing_friendship(
    actor: User, user: User
) -> DefaultFriendshipStatus:
    """Returns the friendship status for the given users."""
    raise NotImplementedError


def get_mutual_friends_count(actor: User, user: User) -> int:
    """Returns the mutual friends for the given users."""
    query = """
    MATCH (user:User {uid: {user_uid}})-[:ARE_FRIENDS]-(n)-[:ARE_FRIENDS]-(other:User {uid: {other_uid}})
    WHERE user <> n
    RETURN count(n)
    """
    params = dict(user_uid=actor.uid, other_uid=user.uid)
    results, meta = db.cypher_query(query, params)
    mutual_friends_count = results[0][0]

    return mutual_friends_count
