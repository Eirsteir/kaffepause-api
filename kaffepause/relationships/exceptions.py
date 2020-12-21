from django.utils.translation import gettext_lazy as _

from kaffepause.common.exceptions import DefaultError


class RelationshipAlreadyExists(DefaultError):
    default_message = _("This relationship already exists")


class CannotAcceptFriendRequest(DefaultError):
    default_message = _("You cannot accept this friend request")


class FriendRequestDoesNotExist(DefaultError):
    default_message = _("This friend request does not exist")


class CannotRejectFriendRequest(DefaultError):
    default_message = _("You cannot reject this friend request")


class CannotUnfriendUser(DefaultError):
    default_message = _("You cannot unfriend this user, you are not friends")


class CannotFollowUser(DefaultError):
    default_message = _("You cannot follow this user, you are not friends")


class CannotUnfollowUser(DefaultError):
    default_message = _("You cannot unfollow this user, you are not friends")
