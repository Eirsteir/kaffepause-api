from enum import Enum

from kaffepause.common.bases import NeomodelRelationshipEnum


class LocationRelationship(NeomodelRelationshipEnum):
    CHILDREN = "CHILD_OF"


class LocationType(Enum):
    UNIVERSITY = "UNIVERSITY"
    CAMPUS = "CAMPUS"
    HOSPITAL = "HOSPITAL"

    @classmethod
    def choices(cls):
        return {field: member.value for field, member in cls.__members__.items()}
