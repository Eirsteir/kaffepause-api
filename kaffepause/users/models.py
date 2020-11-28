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
        "User", "REQUESTED_FRIEND", model=RelationshipRel
    )
    incoming_friend_requests = RelationshipFrom(
        "User", "REQUESTED_FRIEND", model=RelationshipRel
    )
    blocking = RelationshipTo("User", "BLOCKED", model=RelationshipRel)

    @classmethod
    def get_or_create(cls, object_, *props, **kwargs):
        return super().get_or_create({**object_.__dict__}, **kwargs)

    def send_friend_request(self, to_user):
        """Send a friend request to the given user."""
        return self.outgoing_friend_requests.connect(to_user)

    def cancel_friend_request(self, to_user):
        """Cancel a friend request sent to the given user."""
        return self.outgoing_friend_requests.disconnect(to_user)

    def add_friend(self, other):
        """Disconnect requesting relationships and connect the users as friends."""
        self.outgoing_friend_requests.disconnect(other)
        return self.friends.connect(other)
