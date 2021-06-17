from typing import List

from django.utils.translation import gettext_lazy as _
from neomodel import db

from kaffepause.relationships.enums import NonRelatedRelationship, UserRelationship
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


def relationship_exists(user, other):
    """Returns boolean whether or not a relationship of any kind exists between the given users."""
    query = f"""
    MATCH (user:User)-[:{UserRelationship.ARE_FRIENDS}| {UserRelationship.REQUESTING_FRIENDSHIP}]-(other:User)
    WHERE user.uuid = $user_uuid AND other.uuid = $other_uuid
    RETURN other
    """
    params = dict(user_uuid=user.uuid, other_uuid=other.uuid)
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
    # query = f"""
    # MATCH (subject:User {{uuid: $subject_uuid}})
    # -[r:{UserRelationship.ARE_FRIENDS} | {UserRelationship.REQUESTING_FRIENDSHIP}]
    # -(person:User {{uuid: $person_uuid}})
    # return TYPE(r)
    # """
    #
    # params = dict(subject_uuid=actor.uuid, person_uuid=user.uuid)
    # results, meta = db.cypher_query(query, params)
    # status = results[0][0] if results else str(NonRelatedRelationship.CAN_REQUEST)

    if actor.friends.is_connected(user):
        status = str(UserRelationship.ARE_FRIENDS)
    elif actor.outgoing_friend_requests.is_connected(user):
        status = str(NonRelatedRelationship.OUTGOING_REQUEST)
    elif actor.incoming_friend_requests.is_connected(user):
        status = str(NonRelatedRelationship.INCOMING_REQUEST)
    else:
        status = str(NonRelatedRelationship.CAN_REQUEST)

    return _(status)


def get_social_context_between(actor: User, other: User) -> str:
    mutual_friends_count = get_mutual_friends_count(actor=actor, user=other)
    count = mutual_friends_count if mutual_friends_count else "No"
    return _(f"{count} mutual friends")


def get_mutual_friends_count(actor: User, user: User) -> int:
    """Returns the mutual friends for the given users."""
    query = f"""
    MATCH (subject:User {{uuid: $subject_uuid}})-[:{UserRelationship.ARE_FRIENDS}]-(n)-[:{UserRelationship.ARE_FRIENDS}]-(person:User {{uuid: $person_uuid}})
    WHERE subject <> n
    RETURN count(n)
    """
    params = dict(subject_uuid=actor.uuid, person_uuid=user.uuid)
    results, meta = db.cypher_query(query, params)
    mutual_friends_count = results[0][0]

    return mutual_friends_count
