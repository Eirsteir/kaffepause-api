from typing import Tuple

from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from kaffepause.friendships.exceptions import InvalidFriendshipDeletion
from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.friendships.selectors import (
    friendship_exists,
    get_single_friendship,
)

User = get_user_model()


def create_friendship(
    from_user: User,
    to_user: User,
    status: FriendshipStatus = None,
) -> Friendship:
    """
    Add a friendship from one user to another with the given status,
    which defaults to "requested".
    Adding a friendship is by default symmetrical (akin to friending
    someone on facebook).
    """
    if not status:
        status = FriendshipStatus.objects.requested()

    friendships, created = _get_or_create_friendship(
        from_user, to_user, status
    )

    return friendships


@atomic()
def _get_or_create_friendship(
    from_user: User, to_user: User, status: FriendshipStatus
) -> Tuple[Friendship, bool]:
    """
    Look up a friendship with the given arguments, creating one if necessary.
    Return a tuple of (object, created), where created is a boolean
    specifying whether a friendship was created.

    Ensures there is only one friendship between the users at any given time.
    """
    if friendship_exists(from_user, to_user, symmetrical=True):
        return get_single_friendship(from_user, to_user), False

    return (
        Friendship.objects.create(
            from_user=from_user, to_user=to_user, status=status
        ),
        True,
    )


def delete_friendship(actor: User, user: User):
    """
    Deletes a friendship from one user to another, following some simple rules.

    - Both users should be able to delete a requested friendship
    - Both users should be able to delete an accepted friendship
    - Only the one blocking should be able to delete a blocked friendship
    """
    friendship = get_single_friendship(actor, user)

    if friendship.is_blocked:
        return _attempt_to_delete_blocked_friendship(actor, friendship)

    return friendship.delete()


def _attempt_to_delete_blocked_friendship(actor: User, friendship: Friendship):
    """
    Assures only the one blocking can delete the friendship.

    :raises :class:`InvalidFriendshipDeletion` if the friendship status is not blocked
        or if the one being blocked is acting.
    """
    if not friendship.is_blocked:
        raise InvalidFriendshipDeletion(
            _(
                "Cannot delete a blocked friendship when the friendship is not blocked"
            )
        )

    if actor == friendship.from_user:
        return friendship.delete()

    raise InvalidFriendshipDeletion(
        _("Only the blocking user can delete this friendship")
    )
