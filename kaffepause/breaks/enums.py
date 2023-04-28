from enum import Enum

from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class InvitationReplyStatus(Enum):
    CAN_REPLY = "can reply"
    CANNOT_REPLY = "cannot reply"
    ACCEPTED = "accepted"
    DECLINED = "has declined"
    IGNORED = "has ignored"


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
    REQUESTED_CHANGE = _("Requested change")
    CHANGE_REQUESTED_FOR = _("Change request for")
    ACCEPTED_CHANGE = _("Accepted change")
    DENIED_CHANGE = _("Denied change")
    REQUESTED_LOCATION = _("Requested location")
