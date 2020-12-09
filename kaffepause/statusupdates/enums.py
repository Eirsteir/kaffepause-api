from enum import Enum

from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class StatusUpdateType(Enum):
    INACTIVE = _("Inactive")
    READY_FOR_BREAK = _("Ready for a break")
    FOCUSMODE = _("Focusmode")
    ON_A_BREAK = _("On a break")
    UNKNOWN = _("Unknown")

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class StatusUpdateRelationship(NeomodelRelationshipEnum):
    CURRENT = _("Current")
    PREVIOUS = _("Previous")
