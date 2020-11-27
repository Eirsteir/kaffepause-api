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
    name = StringProperty(unique_index=False, required=True)
    username = StringProperty(unique_index=True)

    friends = Relationship("User", "FRIEND", model=FriendRel)
    outgoing_friend_requests = RelationshipTo(
        "User", "REQUESTED_FRIEND", model=RelationshipRel
    )
    incoming_friend_requests = RelationshipFrom(
        "User", "REQUESTED_FRIEND", model=RelationshipRel
    )
    blocked_users = RelationshipTo("User", "BLOCKED", model=RelationshipRel)
