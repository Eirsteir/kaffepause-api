from datetime import datetime

import pytz
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from neomodel import (
    DateTimeProperty,
    One,
    OneOrMore,
    RelationshipFrom,
    RelationshipTo,
    StructuredNode,
    UniqueIdProperty,
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
from kaffepause.common.utils import fifteen_minutes_from_now, time_from_now


class Break(StructuredNode):
    uid = UniqueIdProperty()
    start_time = DateTimeProperty(default=lambda: fifteen_minutes_from_now())
    participants = RelationshipFrom(USER, BreakRelationship.PARTICIPATED_IN)
    invitation = RelationshipFrom(BREAK_INVITATION, BreakRelationship.REGARDING)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clean()

    def clean(self):
        if timezone.now() >= self.start_time:
            raise InvalidBreakStartTime
        elif self.is_expired:
            raise InvalidBreakStartTime(_("Break must start in minimum 5 minutes"))

    @property
    def is_expired(self):
        return time_from_now(minutes=5) >= self.start_time


class BreakInvitation(StructuredNode):
    uid = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    sender = RelationshipFrom(USER, BreakRelationship.SENT, cardinality=One)
    addressees = RelationshipTo(USER, BreakRelationship.TO, cardinality=OneOrMore)
    subject = RelationshipTo(BREAK, BreakRelationship.REGARDING, cardinality=One)

    acceptees = RelationshipFrom(USER, BreakRelationship.ACCEPTED, model=TimeStampedRel)
    declinees = RelationshipFrom(USER, BreakRelationship.DECLINED, model=TimeStampedRel)

    @property
    def is_expired(self):
        return self.subject.single().is_expired

    def get_subject(self):
        return self.subject.single()

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
