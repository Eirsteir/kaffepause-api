from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from neomodel import (
    DateTimeProperty,
    One,
    OneOrMore,
    RelationshipFrom,
    RelationshipTo,
    StructuredNode,
)

from kaffepause.breaks.enums import BreakRelationship
from kaffepause.breaks.exceptions import (
    AlreadyReplied,
    InvalidBreakStartTime,
    InvitationExpired,
    InvitationNotAddressedAtUser,
)
from kaffepause.common.enums import BREAK, BREAK_INVITATION, USER
from kaffepause.common.models import TimeStampedRel
from kaffepause.common.properties import UUIDProperty
from kaffepause.common.utils import fifteen_minutes_from_now, time_from_now


class Break(StructuredNode):
    uuid = UUIDProperty()
    starting_at = DateTimeProperty(default=lambda: fifteen_minutes_from_now())
    participants = RelationshipFrom(USER, BreakRelationship.PARTICIPATED_IN)
    invitation = RelationshipFrom(BREAK_INVITATION, BreakRelationship.REGARDING)

    @classmethod
    def create(cls, *props, **kwargs):
        cls.clean(*props, **kwargs)
        return super().create(*props, **kwargs)

    def clean(self, *props, **kwargs):
        start_time = self.get("starting_at")
        if timezone.now() >= start_time:
            raise InvalidBreakStartTime
        elif time_from_now(minutes=5) >= start_time:
            raise InvalidBreakStartTime(_("Break must start in minimum 5 minutes"))

    @property
    def is_expired(self):
        return time_from_now(minutes=5) >= self.starting_at

    def get_invitation(self):
        return self.invitation.single()

    def get_participants(self):
        return self.participants.all()


class BreakInvitation(StructuredNode):
    uuid = UUIDProperty()
    created = DateTimeProperty(default=lambda: timezone.now())
    sender = RelationshipFrom(USER, BreakRelationship.SENT, cardinality=One)
    addressees = RelationshipTo(USER, BreakRelationship.TO, cardinality=OneOrMore)
    subject = RelationshipTo(BREAK, BreakRelationship.REGARDING, cardinality=One)

    acceptees = RelationshipFrom(USER, BreakRelationship.ACCEPTED, model=TimeStampedRel)
    declinees = RelationshipFrom(USER, BreakRelationship.DECLINED, model=TimeStampedRel)

    @property
    def is_expired(self):
        return self.get_subject().is_expired

    def get_sender(self):
        return self.sender.single()

    def get_subject(self):
        return self.subject.single()

    def get_addressee_count(self):
        return len(self.addressees.all())

    def accept_on_behalf_of(self, user):
        self.acceptees.connect(user)

    def decline_on_behalf_of(self, user):
        self.declinees.connect(user)

    def ready_for_reply(self, user):
        self._check_expiry()
        self._assert_is_addressed_at_user(user)
        self._assert_user_have_not_replied(user)

    def _check_expiry(self):
        if self.is_expired:
            raise InvitationExpired

    def _assert_is_addressed_at_user(self, user):
        if user not in self.addressees:
            raise InvitationNotAddressedAtUser

    def _assert_user_have_not_replied(self, user):
        has_replied = user in self.acceptees or user in self.declinees

        if has_replied:
            raise AlreadyReplied
