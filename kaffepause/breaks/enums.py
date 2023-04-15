from enum import Enum

from django.db import models
from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class InvitationReplyStatus(Enum):
    CAN_REPLY = "can reply"
    CANNOT_REPLY = "cannot reply"
    HAS_ACCEPTED = "has accepted"
    HAS_DECLINED = "has declined"
    HAS_IGNORED = "has ignored"


class BreakRelationship(NeomodelRelationshipEnum):
    PARTICIPATED_IN = _("Participated in")
    INITIATED = _("Initiated")
    SENT = _("Sent")
    TO = _("To")
    REGARDING = _("Regarding")
    ACCEPTED = _("Accepted")
    DECLINED = _("Declined")
    IGNORED = _("Ignored")
    LOCATED_AT = _("Located at")
