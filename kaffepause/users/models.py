from django.contrib.auth.models import AbstractUser
from django_neomodel import DjangoNode
from neomodel import (
    Relationship,
    RelationshipFrom,
    RelationshipTo,
    StringProperty,
    ZeroOrOne, ZeroOrMore,
)

from kaffepause.breaks.enums import BreakRelationship
from kaffepause.common.enums import (
    BREAK,
    BREAK_INVITATION,
    LOCATION,
    STATUS_UPDATE,
    USER, NOTIFICATION,
)
from kaffepause.common.properties import UUIDProperty
from kaffepause.location.enums import LocationRelationship
from kaffepause.notifications.enums import NotificationRelationship
from kaffepause.relationships.enums import UserRelationship
from kaffepause.relationships.models import FriendRel, RelationshipRel
from kaffepause.statusupdates.enums import StatusUpdateRelationship


class User(DjangoNode):
    uuid = UUIDProperty()
    name = StringProperty(required=True, index=True, max_length=100)
    username = StringProperty(unique_index=True, max_length=100)
    locale = StringProperty(default="en_US", max_length=10)
    profile_pic = StringProperty()

    friends = Relationship(USER, UserRelationship.ARE_FRIENDS, model=FriendRel)
    following = RelationshipTo(USER, UserRelationship.FOLLOWING, model=RelationshipRel)
    followed_by = RelationshipFrom(
        USER, UserRelationship.FOLLOWING, model=RelationshipRel
    )

    outgoing_friend_requests = RelationshipTo(
        USER, UserRelationship.REQUESTING_FRIENDSHIP, model=RelationshipRel
    )
    incoming_friend_requests = RelationshipFrom(
        USER, UserRelationship.REQUESTING_FRIENDSHIP, model=RelationshipRel
    )

    breaks = RelationshipTo(BREAK, BreakRelationship.PARTICIPATED_IN)
    break_invitations = RelationshipFrom(BREAK_INVITATION, BreakRelationship.TO)
    sent_break_invitations = RelationshipTo(BREAK_INVITATION, BreakRelationship.SENT)
    accepted_break_invitations = RelationshipTo(
        BREAK_INVITATION, BreakRelationship.ACCEPTED
    )
    declined_break_invitations = RelationshipTo(
        BREAK_INVITATION, BreakRelationship.DECLINED
    )

    current_status = RelationshipTo(
        STATUS_UPDATE, StatusUpdateRelationship.CURRENT, cardinality=ZeroOrOne
    )

    preferred_location = RelationshipTo(
        LOCATION, LocationRelationship.PREFERRED_LOCATION, cardinality=ZeroOrOne
    )
    current_location = RelationshipTo(
        LOCATION, LocationRelationship.CURRENT_LOCATION, cardinality=ZeroOrOne
    )

    notifications = RelationshipFrom(
        NOTIFICATION, NotificationRelationship.NOTIFIES, cardinality=ZeroOrMore
    )

    class Meta:
        app_label = "users"

    @classmethod
    def get_or_create(cls, object_, *props, **kwargs):
        return super().get_or_create({**object_.__dict__}, **kwargs)

    def send_friend_request(self, addressee):
        """Send a friend request to the given user."""
        return self.outgoing_friend_requests.connect(addressee)

    def cancel_friend_request(self, addressee):
        """Cancel a friend request sent to the given user."""
        return self.outgoing_friend_requests.disconnect(addressee)

    def reject_friend_request(self, requester):
        """Reject a friend request sent from the given user."""
        return self.incoming_friend_requests.disconnect(requester)

    def is_friends_with(self, user):
        return self.friends.is_connected(user)

    def has_send_friend_request_to(self, user):
        return self.outgoing_friend_requests.is_connected(user)

    def add_friend(self, other):
        """Disconnect requesting relationships and connect the users as friends."""
        self.outgoing_friend_requests.disconnect(other)
        self.following.connect(other)
        other.following.connect(self)
        return self.friends.connect(other)

    def remove_friend(self, friend):  # Returns None if not friends - ok?
        """Disconnect self and friend."""
        self.following.disconnect(friend)
        friend.following.disconnect(self)
        return self.friends.disconnect(friend)

    def can_perform_action_on_friend(self, friend):
        """A user can perform an arbitrary action on another if they are friends and the friend is not itself."""
        return self.friends.is_connected(friend) and friend is not self

    def follow_user(self, user):
        return self.following.connect(user)

    def unfollow_user(self, user):
        return self.following.disconnect(user)

    def get_current_status(self):
        return self.current_status.single()

    def get_preferred_location(self):
        return self.preferred_location.single()

    def get_current_location(self):
        return self.current_location.single()

    def is_initiator_of(self, break_):
        return self.sent_break_invitations.is_connected(break_.get_invitation())

    def is_participant_of(self, break_):
        return self.breaks.is_connected(break_)

    @property
    def short_name(self):
        return self.name.split()[0]
