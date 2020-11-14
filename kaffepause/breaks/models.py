from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from kaffepause.breaks.enums import InvitationReply
from kaffepause.breaks.exceptions import (
    BreakInvitationExpiresBeforeStartTime,
    InvitationExpired,
)
from kaffepause.common.models import StatusModel

User = get_user_model()


class Break(TimeStampedModel):
    participants = models.ManyToManyField(
        User, related_name="breaks", related_query_name="break"
    )
    start_time = models.TimeField(default=timezone.now() + timedelta(minutes=30))


class BreakInvitation(TimeStampedModel):
    """Model class for inviting to a break from studies. The invitation expires in 3 hours from time of creation by default."""

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
    # TODO: change name?
    subject = models.ForeignKey(
        Break, on_delete=models.CASCADE, related_name="invitations"
    )
    message = models.CharField(max_length=75, null=True, blank=True)

    # location?
    is_seen = models.BooleanField(default=False)
    reply = models.CharField(
        choices=InvitationReply.choices, max_length=10, null=True, blank=True
    )
    expiry = models.TimeField(
        default=timezone.now() + timedelta(hours=3)
    )  # TODO: put in settings?

    class Meta:
        ordering = ("-created", "is_seen")
        verbose_name = _("Break invitation")
        verbose_name_plural = _("Break invitations")
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "recipient", "subject"], name="unique-invitation"
            )
        ]

    @atomic
    def accept(self):
        self.check_expiry()
        self.reply = InvitationReply.ACCEPTED
        self.subject.participants.add(self.recipient)
        self.save()

    def decline(self):
        self.check_expiry()
        self.reply = InvitationReply.DECLINED
        self.save()

    def ignore(self):
        self.check_expiry()
        self.reply = InvitationReply.IGNORED
        self.save()

    def check_expiry(self):
        if self.is_expired:
            raise InvitationExpired

    @property
    def is_expired(self):
        return self.expiry >= localtime().time()


class BreakHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="previous_breaks"
    )
    related_break = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="history+"
    )

    class Meta:
        verbose_name = _("Break history")
        verbose_name_plural = _("Break histories")
