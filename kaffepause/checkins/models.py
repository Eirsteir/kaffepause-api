from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from kaffepause.checkins.enums import Intensity
from kaffepause.common.models import StatusManager, StatusModel

User = get_user_model()


class CheckInStatusManager(StatusManager):
    pass


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

    class Meta:
        verbose_name = _("Check-in")
        verbose_name_plural = _("Check-ins")
