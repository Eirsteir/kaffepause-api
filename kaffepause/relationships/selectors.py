from typing import List, Union

from django.db.models import Q, QuerySet

from kaffepause.relationships.models import Relationship, RelationshipStatus
from kaffepause.users.models import User


def get_relationships_for(
    user: User, status: RelationshipStatus, symmetrical: bool = True
) -> Union[QuerySet, List[User]]:
    """
    Returns a QuerySet of user objects with which the given user has
    established a relationship.
    """

    query = _get_incoming_query(user, status)

    if symmetrical:
        query |= _get_outgoing_query(user, status)

    return User.objects.filter(query)


def get_incoming_relationships_for(
    user: User, status: RelationshipStatus
) -> Union[QuerySet, List[User]]:
    """
    Returns a QuerySet of user objects which have created a relationship to
    the given user. to_user = user, from_user = other_user
    """
    return User.objects.filter(_get_incoming_query(user, status))


def get_outgoing_relationships_for(
    user: User, status: RelationshipStatus
) -> Union[QuerySet, List[User]]:
    """Returns a QuerySet of user objects which the given user has created a relationship to."""
    return User.objects.filter(_get_outgoing_query(user, status))


def _get_incoming_query(user, status):
    return Q(from_users__to_user=user, from_users__status=status)


def _get_outgoing_query(user, status):
    return Q(to_users__from_user=user, to_users__status=status)


def relationship_exists(from_user, to_user, status=None, symmetrical=False):
    """
    Returns boolean whether or not a relationship exists between the given
    users.  An optional :class:`RelationshipStatus` instance can be specified.

    If symmetrical = True the reversed relationships existence is also queried for.
    """

    query = Q(from_user=from_user, to_user=to_user)

    if status:
        query &= Q(status=status)

    if symmetrical:
        query |= Q(from_user=to_user, to_user=from_user)

        if status:
            query &= Q(status=status)

    return Relationship.objects.filter(query).exists()


def following(user):
    return get_relationships_for(user, RelationshipStatus.objects.requesting())


def followers(user):
    return get_incoming_relationships_for(
        user, RelationshipStatus.objects.requesting()
    )


def blocking(user):
    return get_outgoing_relationships_for(
        user, RelationshipStatus.objects.blocked()
    )


def blockers(user):
    return get_incoming_relationships_for(
        user, RelationshipStatus.objects.blocked()
    )


def friends(user):
    return get_relationships_for(
        user, RelationshipStatus.objects.friends(), True
    )
