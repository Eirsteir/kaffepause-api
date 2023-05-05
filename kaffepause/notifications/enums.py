from enum import Enum

from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class SeenState(Enum):
    UNSEEN = "unseen"
    UNREAD = "unread"
    SEEN = "seen"
    SEEN_AND_READ = "seen and read"

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class NotificationEntityType(Enum):
    USER_FRIEND_ADD = _("User sends a friend request")
    USER_FRIEND_ACCEPT = _("User accepts a friend request")
    BREAK_INVITATION_SENT_INDIVIDUALLY = _("Individual break invitation is sent")
    BREAK_INVITATION_SENT_TO_GROUP = _("Group break invitation is sent")
    BREAK_INVITATION_ACCEPTED = _("Break invitation is accepted")
    BREAK_INVITATION_DECLINED = _("Break invitation is declined")
    GROUP_MEMBER_ADDED = _("User is added to group")

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class NotificationRelationship(NeomodelRelationshipEnum):
    NOTIFIES = _("Notifies")
    ACTOR = _("Is actor of")
    SUBJECT = _("Is about")


