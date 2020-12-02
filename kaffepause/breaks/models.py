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
    InvalidInvitationExpiration,
    InvitationExpired,
    InvitationNotAddressedAtUser,
)
from kaffepause.common.enums import Node
from kaffepause.common.utils import fifteen_minutes_from_now, time_from_now


class Break(StructuredNode):
    uid = UniqueIdProperty()
    start_time = DateTimeProperty(default=lambda: fifteen_minutes_from_now())
    participants = RelationshipFrom(Node.USER, BreakRelationship.PARTICIPATED_IN)

    def clean_fields(self, *args, **kwargs):
        if not self.start_time:
            self.start_time = fifteen_minutes_from_now()
        return super().clean_fields(*args, **kwargs)

    def clean(self):
        if timezone.now() >= self.start_time:
            raise InvalidBreakStartTime


class BreakInvitation(StructuredNode):
    uid = UniqueIdProperty()
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    sender = RelationshipFrom(Node.USER, BreakRelationship.SENT, cardinality=One)
    addressees = RelationshipTo(Node.USER, BreakRelationship.TO, cardinality=OneOrMore)
    subject = RelationshipTo(Node.BREAK, BreakRelationship.REGARDING, cardinality=One)

    acceptees = RelationshipFrom(Node.USER, BreakRelationship.ACCEPTED)
    declinees = RelationshipFrom(Node.USER, BreakRelationship.DECLINED)

    def clean_fields(self, *args, **kwargs):
        if self.is_expired:
            raise InvalidInvitationExpiration(
                _("Invitation expiry must be in the future")
            )
        return super().clean_fields(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return time_from_now(minutes=5) >= self.subject

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
