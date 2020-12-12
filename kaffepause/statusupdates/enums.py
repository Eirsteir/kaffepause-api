from enum import Enum

from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class StatusUpdateType(Enum):
    INACTIVE = _("is inactive")
    READY_FOR_BREAK = _("is ready for a break")
    FOCUSMODE = _("is in focusmode")
    ON_A_BREAK = _("is on a break")
    UNKNOWN = _("is MIA")

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class StatusUpdateRelationship(NeomodelRelationshipEnum):
    CURRENT = _("Current")
    PREVIOUS = _("Previous")
