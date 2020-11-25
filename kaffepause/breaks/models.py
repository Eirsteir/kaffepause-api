from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from kaffepause.breaks.enums import InvitationReply
from kaffepause.breaks.exceptions import (
    AlreadyReplied,
    InvalidBreakStartTime,
    InvalidInvitationExpiration,
    InvitationExpired,
)
from kaffepause.common.models import StatusModel
from kaffepause.common.utils import thirty_minutes_from_now, three_hours_from_now

User = get_user_model()


class Break(TimeStampedModel):
    participants = models.ManyToManyField(
        User, related_name="breaks", related_query_name="break"
    )
    start_time = models.DateTimeField(default=thirty_minutes_from_now)

    @property
    def actual_start_time(self):
        return datetime.combine(self.created, self.start_time.time())

    def clean_fields(self, *args, **kwargs):
        if not self.start_time:
            self.start_time = thirty_minutes_from_now()
        return super().clean_fields(*args, **kwargs)

    def clean(self):
        if timezone.now() >= self.start_time:
            raise InvalidBreakStartTime

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def add_participant(self, participant):
        self.participants.add(participant)

    def __str__(self):
        return f"Break starting at {self.actual_start_time} ({self.participants.count()} participants)"


class BreakInvitation(TimeStampedModel):
    # inviter, requester, sender, actor,
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invites"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="break_invites",
        related_query_name="break_invitation",
    )
    subject = models.ForeignKey(
        Break, on_delete=models.CASCADE, related_name="invitations"
    )
    message = models.CharField(max_length=75, null=True, blank=True)

    # location?
    is_seen = models.BooleanField(default=False)
    reply = models.CharField(
        choices=InvitationReply.choices, max_length=10, null=True, blank=True
    )
    expiry = models.DateTimeField(default=three_hours_from_now)

    class Meta:
        ordering = ("-created", "is_seen")
        verbose_name = _("Break invitation")
        verbose_name_plural = _("Break invitations")
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "recipient", "subject"], name="unique-invitation"
            )
        ]

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
        return timezone.now() >= self.expiry

    @atomic
    def accept(self):
        self._reply(InvitationReply.ACCEPTED)
        self.subject.add_participant(self.recipient)

    def decline(self):
        self._reply(InvitationReply.DECLINED)

    def ignore(self):
        self._reply(InvitationReply.IGNORED)

    def _reply(self, reply: InvitationReply):
        self.check_expiry()
        self.assert_is_not_already_replied_to()
        self.reply = reply
        self.save()

    def check_expiry(self):
        if self.is_expired:
            raise InvitationExpired

    def assert_is_not_already_replied_to(self):
        if self.reply:
            raise AlreadyReplied

    def __str__(self):
        return f"Invitation from {self.sender} to {self.recipient}, {self.subject}"


class BreakHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="previous_breaks"
    )
    subject = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history+")

    class Meta:
        verbose_name = _("Break history")
        verbose_name_plural = _("Break histories")

    def __str__(self):
        return f"{self.user} - {self.subject}"
