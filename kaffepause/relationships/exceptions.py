from django.utils.translation import gettext_lazy as _

from kaffepause.common.exceptions import DefaultError


class RelationshipAlreadyExists(DefaultError):
    default_message = _("Relationship already exists")


class CannotAcceptFriendRequest(DefaultError):
    default_message = _("Cannot accept this friend request")


class CannotCancelFriendRequest(DefaultError):
    default_message = _("Cannot cancel this friend request")


class CannotRejectFriendRequest(DefaultError):
    default_message = _("Cannot reject this friend request")


class CannotUnfriendUser(DefaultError):
    default_message = _("Cannot unfriend this user. The users have to be friends")


class CannotFollowUser(DefaultError):
    default_message = _("Cannot follow this user. The users have to be friends")


class CannotUnfollowUser(DefaultError):
    default_message = _("Cannot unfollow this user. The users have to be friends")
