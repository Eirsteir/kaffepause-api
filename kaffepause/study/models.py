from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from kaffepause.common.models import StatusModel
from kaffepause.study.enums import Intensity, InvitationReply

User = get_user_model()


# TODO: Split CheckIn and Break into separate apps?
class CheckInStatus(StatusModel):
    class Meta:
        verbose_name = _("Check-in status")
        verbose_name_plural = _("Check-in statuses")


class CheckIn(TimeStampedModel):
    """Model class for a users current action - what the user is currently doing."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="check_ins",
        verbose_name=_("check-ins"),
    )
    status = models.ForeignKey(
        CheckInStatus, on_delete=models.PROTECT, verbose_name=_("status")
    )
    intensity = models.CharField(
        choices=Intensity.choices, max_length=14, blank=False, default=Intensity.FOCUSED
    )
    duration = models.DurationField(default=timedelta(minutes=50))


class Break(TimeStampedModel):
    participants = models.ManyToManyField(
        User, related_name="breaks", related_query_name="break"
    )


class BreakInvitation(TimeStampedModel):
    """Model class for inviting to a break from studies."""

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
    start_time = models.TimeField(default=timezone.now() + timedelta(minutes=30))
    # location?
    is_seen = models.BooleanField(default=False)
    reply = models.CharField(
        choices=InvitationReply.choices, max_length=10, null=True, blank=True
    )
    expiry = models.TimeField(default=timezone.now() + timedelta(hours=3))

    class Meta:
        ordering = ("-created", "is_seen")
        verbose_name = _("Break invitation")
        verbose_name_plural = _("Break invitations")

    @property
    def is_expired(self):
        return self.expiry >= localtime().time()

    def accept(self):

        pass

    def decline(self):
        pass

    def ignore(self):
        pass

    def delete(self, using=None, keep_parents=False):
        pass


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
