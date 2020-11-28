from django.contrib.auth.models import AbstractUser
from neomodel import (
    Relationship,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)

from kaffepause.relationships.models import FriendRel, RelationshipRel


class User(StructuredNode):
    uid = (
        UniqueIdProperty()
    )  # https://neomodel.readthedocs.io/en/latest/properties.html#independent-database-property-name
    name = StringProperty(required=True, index=True)
    username = StringProperty(unique_index=True)

    friends = Relationship("User", "ARE_FRIENDS", model=FriendRel)
    outgoing_friend_requests = RelationshipTo(
        "User", "REQUESTED_TO_FRIEND", model=RelationshipRel
    )
    incoming_friend_requests = RelationshipFrom(
        "User", "REQUESTED_FROM_FRIEND", model=RelationshipRel
    )
    blocked_users = RelationshipTo("User", "BLOCKED", model=RelationshipRel)

    @classmethod
    def get_or_create(cls, object_, *props, **kwargs):
        return super().get_or_create({**object_.__dict__}, **kwargs)
