from typing import Any

from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from neomodel import db

from kaffepause.relationships.exceptions import InvalidFriendshipDeletion
from kaffepause.users.models import User


def send_friend_request(actor: User, to_user: User) -> User:
    query = "MATCH (a:User)-[:FRIEND | :REQUESTED_FRIEND]-(b:User) WHERE a.id = {actor_id} AND b.id = {to_user_id} RETURN b"
    params = dict(actor_id=actor.id, to_user_id=to_user.id)
    results, meta = db.cypher_query(query, params)
    people = [User.inflate(row[0]) for row in results]
    print(people)

    actor.outgoing_friend_requests.connect(to_user)
    to_user.incoming_friend_requests.connect(actor)
    return to_user


def create_friendship(from_user, to_user):
    raise NotImplementedError()


def accept_friend_request(actor: User, from_user: User) -> Any:
    """Create a friendship relationship between given nodes."""
    actor.incoming_friend_requests.relationships(from_user)
    raise NotImplementedError()


@atomic()
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
