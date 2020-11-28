from django.utils.translation import gettext_lazy as _

from kaffepause.common.exceptions import DefaultError


class RelationshipAlreadyExists(DefaultError):
    default_message = _("Relationship already exists")


class CannotAcceptFriendRequest(DefaultError):
    default_message = _("Cannot accept this friend request")


class InvalidFriendshipDeletion(DefaultError):
    pass


class InvalidFriendshipStatusChange(DefaultError):
    pass


class UnnecessaryStatusUpdate(DefaultError):
    pass
