from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from kaffepause.breaks.enums import InvitationReply
from kaffepause.breaks.exceptions import InvitationExpired
from kaffepause.common.models import StatusModel
from kaffepause.common.utils import thirty_minutes_from_now, three_hours_from_now

User = get_user_model()


class Break(TimeStampedModel):
    participants = models.ManyToManyField(
        User, related_name="breaks", related_query_name="break"
    )
    start_time = models.TimeField(default=thirty_minutes_from_now)

    @property
    def actual_start_time(self):
        actual_start_time = self.created
        actual_start_time.replace(hour=self.start_time.hour)
        actual_start_time.replace(minute=self.start_time.minute)
        actual_start_time.replace(second=self.start_time.second)
        return actual_start_time

    def __str__(self):
        return f"Break starting at {self.actual_start_time} ({self.participants.count()} participants)"


class BreakInvitation(TimeStampedModel):
    """
    Model class for inviting to a break from studies.
    The invitation expires in 3 hours from time of creation by default.
    """

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
    expiry = models.TimeField(default=three_hours_from_now)  # TODO: put in settings?

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
