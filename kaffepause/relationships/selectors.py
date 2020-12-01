from typing import List

from django.utils.translation import gettext_lazy as _
from neomodel import db

from kaffepause.relationships.enums import (
    ARE_FRIENDS,
    CAN_REQUEST,
    REQUESTING_FRIENDSHIP,
)
from kaffepause.users.models import User


def get_friends_count(user: User) -> int:
    return len(get_friends(user))


def get_friends(user: User) -> List[User]:
    # TODO: exclude current user
    return user.friends.all()


def get_incoming_requests(
    user: User,
) -> List[User]:
    return user.incoming_friend_requests.all()


def get_outgoing_requests(
    user: User,
) -> List[User]:
    return user.outgoing_friend_requests.all()


def relationship_exists(user, other):
    """Returns boolean whether or not a relationship of any kind exists between the given users."""
    query = f"""
    MATCH (user:User)-[:{ARE_FRIENDS}| :{REQUESTING_FRIENDSHIP}]-(other:User)
    WHERE user.uid = {{user_uid}} AND other.uid = {{other_uid}}
    RETURN other
    """
    params = dict(user_uid=user.uid, other_uid=other.uid)
    results, meta = db.cypher_query(query, params)
    people = [User.inflate(row[0]) for row in results]
    return people


def get_friendship_status(actor: User, user: User) -> object:
    """
    Returns the friendship status as viewed by the actor.
    If no such friendship exists, a default value of 'CAN_REQUEST' is returned.
    """
    # TODO: Differ between requested direction
    if actor == user:
        return

    query = f"""
    MATCH (subject:User {{uid: {{subject_uid}}}})-[r:{ARE_FRIENDS} | :{REQUESTING_FRIENDSHIP}]-(person:User {{uid: {{person_uid}}}})
    return TYPE(r)
    """

    params = dict(subject_uid=actor.uid, person_uid=user.uid)
    results, meta = db.cypher_query(query, params)
    status = results[0][0] if results else None

    if status:
        return _(status)

    return CAN_REQUEST


def get_social_context_between(actor: User, other: User) -> str:
    mutual_friends_count = get_mutual_friends_count(actor=actor, user=other)
    count = mutual_friends_count if mutual_friends_count else "No"
    return _(f"{count} mutual friends")


def get_mutual_friends_count(actor: User, user: User) -> int:
    """Returns the mutual friends for the given users."""
    query = f"""
    MATCH (subject:User {{uid: {{subject_uid}}}})-[:{ARE_FRIENDS}]-(n)-[:{ARE_FRIENDS}]-(person:User {{uid: {{person_uid}}}})
    WHERE subject <> n
    RETURN count(n)
    """
    params = dict(subject_uid=actor.uid, person_uid=user.uid)
    results, meta = db.cypher_query(query, params)
    mutual_friends_count = results[0][0]

    return mutual_friends_count
