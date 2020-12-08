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
        return ({tag.name, tag.value} for tag in cls)


class StatusUpdateRelationship(NeomodelRelationshipEnum):
    CURRENT = _("Current")
    PREVIOUS = _("Previous")
