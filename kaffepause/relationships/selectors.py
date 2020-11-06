from typing import List, Union

from django.db.models import Q, QuerySet

from kaffepause.relationships.models import RelationshipStatus
from kaffepause.users.models import User


def get_friendships(
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


def _get_incoming_query(user, status):
    return Q(to_users__from_user=user, to_users__status=status)


def _get_outgoing_query(user, status):
    return Q(from_users__to_user=user, from_users__status=status)


# TODO: remove?
def incoming_friendships(user, status):
    """
    Returns a QuerySet of user objects who have created a relationship to
    the given user, but which the given user has not reciprocated
    """
    from_relationships = get_friendships(user, status)
    to_relationships = get_related_to(user, status)
    return to_relationships.exclude(pk__in=from_relationships.values_list("pk"))


# TODO: remove?
def outgoing_friendships(user, status):
    """
    Like :method:`only_to`, returns user objects with whom the given user
    has created a relationship, but which have not reciprocated
    """
    from_relationships = get_friendships(user, status)
    to_relationships = get_related_to(user, status)
    return from_relationships.exclude(pk__in=to_relationships.values_list("pk"))


def get_related_to(
    user: User, status: RelationshipStatus
) -> Union[QuerySet, List[User]]:
    """
    Returns a QuerySet of user objects which have created a relationship to
    the given user.
    """
    return User.objects.filter(**_get_outgoing_query(user, status))


def friendship_exists(user, other_user, status=None, symmetrical=False):
    """
    Returns boolean whether or not a relationship exists between the given
    users.  An optional :class:`RelationshipStatus` instance can be specified.
    """
    query = dict(to_users__from_user=user, to_users__to_user=other_user)

    if status:
        query.update(to_users__status=status)

    if symmetrical:
        query.update(from_users__to_user=user, from_users__from_user=other_user)

        if status:
            query.update(from_users__status=status)

    return User.objects.filter(**query).exists()


def following(user):
    return get_friendships(user, RelationshipStatus.objects.requesting())


def followers(user):
    return get_related_to(user, RelationshipStatus.objects.requesting())


def blocking(user):
    return get_friendships(user, RelationshipStatus.objects.blocked())


def blockers(user):
    return get_related_to(user, RelationshipStatus.objects.blocked())


def friends(user):
    return get_friendships(user, RelationshipStatus.objects.friends(), True)


# def get_relationships(self, status):
#     return self.friends.filter(to_people__status=status, to_people__from_user=self)


# def get_friends_of(user: User) -> Union[QuerySet, List[User]]:
#     """Return all users who are in an accepted friendship relation with the given user."""
#     return get_friend_relation_of_user_with_status(user, FriendshipStatus.ACCEPTED)
#
#
# def get_friend_relation_of_user_with_status(
#     user: User, status: FriendshipStatus
# ) -> Union[QuerySet, List[User]]:
#     """Return all users who are in a friendship relation with the given user and with the given status."""
#     other_user_query = Q(friendship_requested_by_user__to_user=user) | Q(
#         friendship_addressed_at_user__from_user=user
#     )
#     status_query = Q(friendship_requested_by_user__status=status) | Q(
#         friendship_addressed_at_user__status=status
#     )
#
#     return User.objects.filter(other_user_query & status_query)
#
#
# def get_incoming_friend_requests_for(user: User) -> Union[QuerySet, List[User]]:
#     """Return all users who has sent a friend request to given user."""
#     status_query = Q(friendship_addressed_at_user__status=FriendshipStatus.REQUESTED)
#     return query_friends_of(user, status_query)
#
#
# def get_outgoing_friend_requests_for(user: User) -> Union[QuerySet, List[User]]:
#     """Return all users who given user has sent a friend request to."""
#     status_query = Q(
#         friends__friendship_addressed_at_user__status=FriendshipStatus.REQUESTED
#     )
#     return query_friends_of(user, status_query)
#
#
# def query_friends_of(user: User, query: Q) -> Union[QuerySet, List[User]]:
#     return user.friends.filter(query)
