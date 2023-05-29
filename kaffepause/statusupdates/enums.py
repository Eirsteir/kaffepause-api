from enum import Enum

from django.utils.translation import gettext as _

from kaffepause.common.bases import NeomodelRelationshipEnum


class StatusUpdateType(Enum):
    INACTIVE = "is inactive"
    READY_FOR_BREAK = "is ready for a break"
    FOCUSMODE = "is in focusmode"
    ON_A_BREAK = "is on a break"
    UNKNOWN = "is MIA"

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}


class StatusUpdateRelationship(NeomodelRelationshipEnum):
    CURRENT = "Current"
    PREVIOUS = "Previous"
