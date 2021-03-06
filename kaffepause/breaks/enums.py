from django.db import models
from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class InvitationReply(models.TextChoices):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    IGNORED = "ignored"


class BreakRelationship(NeomodelRelationshipEnum):
    PARTICIPATED_IN = _("Participated in")
    SENT = _("Sent")
    TO = _("To")
    REGARDING = _("Regarding")
    ACCEPTED = _("Accepted")
    DECLINED = _("Declined")
