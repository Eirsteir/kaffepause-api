from django.db import models
from neomodel import StructuredNode, StringProperty, RelationshipTo, OneOrMore, RelationshipFrom, One

from kaffepause.common.enums import USER
from kaffepause.common.models import TimeStampedNode
from kaffepause.common.properties import UUIDProperty
from kaffepause.groups.enums import GroupRelationship


class Group(TimeStampedNode):
    uuid = UUIDProperty()
    name = StringProperty(required=True)
    members = RelationshipTo(USER, GroupRelationship.HAS_MEMBER, cardinality=OneOrMore)
    creator = RelationshipFrom(USER, GroupRelationship.CREATED_GROUP, cardinality=One)
