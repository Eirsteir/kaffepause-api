from django.contrib.auth import get_user_model

from kaffepause.relationships.enums import RelationshipStatusEnum
from kaffepause.relationships.models import Relationship, RelationshipStatus

User = get_user_model()


def create_relationship(
    from_user: User,
    to_user: User,
    status: RelationshipStatus = None,
    symmetrical: bool = True,
):
    """
    Add a relationship from one user to another with the given status,
    which defaults to "following".
    Adding a relationship is by default symmetrical (akin to friending
    someone on facebook). Specify an asymmetrical relationship (akin to following
    on twitter) by passing in :param:`symmetrical` = False
    .. note::
        If :param:`symmetrical` is set, the function will return a tuple
        containing the two relationship objects created
    """
    if not status:
        status = RelationshipStatus.objects.requested()

    relationship, created = Relationship.objects.get_or_create(
        from_user=from_user, to_user=to_user, status=status
    )

    if symmetrical:
        return relationship, create_relationship(from_user, to_user, status, False)

    return relationship


def delete_relationship_from_to(
    from_user: User,
    to_user: User,
    status: RelationshipStatusEnum = None,
    symmetrical: bool = True,
):
    """
    Remove a relationship from one user to another, with the same caveats
    and behavior as adding a relationship.
    """
    if not status:
        status = RelationshipStatus.objects.requested()

    result = Relationship.objects.filter(
        from_user=from_user, to_user=to_user, status=status
    ).delete()

    if symmetrical:
        return result, delete_relationship_from_to(to_user, from_user, status, False)

    return result
