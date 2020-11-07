from typing import Tuple

from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _

from kaffepause.relationships.exceptions import InvalidRelationshipDeletion
from kaffepause.relationships.models import Relationship, RelationshipStatus
from kaffepause.relationships.selectors import (
    get_single_relationship,
    relationship_exists,
)

User = get_user_model()


def create_relationship(
    from_user: User,
    to_user: User,
    status: RelationshipStatus = None,
) -> Relationship:
    """
    Add a relationship from one user to another with the given status,
    which defaults to "requested".
    Adding a relationship is by default symmetrical (akin to friending
    someone on facebook).
    """
    if not status:
        status = RelationshipStatus.objects.requested()

    relationship, created = _get_or_create_relationship(
        from_user, to_user, status
    )

    return relationship


@atomic()
def _get_or_create_relationship(
    from_user: User, to_user: User, status: RelationshipStatus
) -> Tuple[Relationship, bool]:
    """
    Look up a relationship with the given arguments, creating one if necessary.
    Return a tuple of (object, created), where created is a boolean
    specifying whether a relationship was created.

    Ensures there is only one relationship between the users at any given time.
    """
    if relationship_exists(from_user, to_user, symmetrical=True):
        return get_single_relationship(from_user, to_user), False

    return (
        Relationship.objects.create(
            from_user=from_user, to_user=to_user, status=status
        ),
        True,
    )


def delete_relationship(actor: User, user: User):
    """
    Deletes a relationship from one user to another, following some simple rules.

    - Both users should be able to delete a requested relationship
    - Both users should be able to delete an accepted relationship
    - Only the one blocking should be able to delete a blocked relationship
    """
    relationship = get_single_relationship(actor, user)

    if relationship.is_blocked:
        return _attempt_to_delete_blocked_relationship(actor, relationship)

    return relationship.delete()


def _attempt_to_delete_blocked_relationship(
    actor: User, relationship: Relationship
):
    """
    Assures only the one blocking can delete the relationship.

    :raises :class:`InvalidRelationshipDeletion` if the relationship status is not blocked
        or if the one being blocked is acting.
    """
    if not relationship.is_blocked:
        raise InvalidRelationshipDeletion(
            _(
                "Cannot delete a blocked relationship when the relationship is not blocked"
            )
        )

    if actor == relationship.from_user:
        return relationship.delete()

    raise InvalidRelationshipDeletion(
        _("Only the blocking user can delete this relationship")
    )
