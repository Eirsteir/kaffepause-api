from enum import Enum

from django.db import models
from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum
from kaffepause.common.enums import Endpoints


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
    BREAK_INVITATION_SENT = _("Break invitation is sent")
    BREAK_INVITATION_ACCEPTED = _("Break invitation is accepted")
    BREAK_INVITATION_DECLINED = _("Break invitation is declined")

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class NotificationRelationship(NeomodelRelationshipEnum):
    NOTIFIES = _("Notifies")
    ACTOR = _("Is actor of")
    SUBJECT = _("Is about")


entityTypeToEndpointMapping = {
    NotificationEntityType.USER_FRIEND_ADD: Endpoints.USERS,
    NotificationEntityType.USER_FRIEND_ACCEPT: Endpoints.USERS,
    NotificationEntityType.BREAK_INVITATION_SENT: Endpoints.BREAKS,
}
