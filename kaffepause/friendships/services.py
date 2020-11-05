from django.contrib.auth import get_user_model

from kaffepause.friendships.models import Friendship, RelationshipStatus

User = get_user_model()


def create_friendship(user, other_user, status=None, symmetrical=True):
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
        status = RelationshipStatus.objects.following()

    relationship, created = Friendship.objects.get_or_create(
        requester=user, addressee=other_user, status=status
    )

    if symmetrical:
        return relationship, create_friendship(user, other_user, status, False)
    else:
        return relationship


def delete_friendship(user, other_user, status=None, symmetrical=True):
    """
    Remove a relationship from one user to another, with the same caveats
    and behavior as adding a relationship.
    """
    if not status:
        status = RelationshipStatus.objects.requesting()

    res = Friendship.objects.filter(
        requester=user, addressee=other_user, status=status
    ).delete()

    if symmetrical:
        return res, delete_friendship(other_user, user, status, False)
    else:
        return res
