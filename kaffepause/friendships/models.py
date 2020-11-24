from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel

from kaffepause.common.models import StatusManager, StatusModel
from kaffepause.friendships.enums import DefaultFriendshipStatus

User = get_user_model()


class FriendshipsStatusManager(StatusManager):
    def requested(self):
        return self.get(slug=DefaultFriendshipStatus.REQUESTED())

    def blocked(self):
        return self.get(slug=DefaultFriendshipStatus.BLOCKED())

    def friends(self):
        return self.get(slug=DefaultFriendshipStatus.ARE_FRIENDS())


class FriendshipStatus(StatusModel):

    from_slug = models.CharField(
        _("from slug"),
        max_length=100,
        help_text=_("Denote the friendship from the user, i.e. user is 'requesting'"),
    )
    to_slug = models.CharField(
        _("to slug"),
        max_length=100,
        help_text=_("Denote the friendship to the user, i.e. user is 'requested' by"),
    )

    login_required = models.BooleanField(
        _("login required"),
        default=False,
        help_text=_("Users must be logged in to see these friendship"),
    )
    private = models.BooleanField(
        _("private"),
        default=False,
        help_text=_("Only the user who owns these friendship can see them"),
    )

    objects = FriendshipsStatusManager()

    class Meta:
        verbose_name = _("Friendship status")
        verbose_name_plural = _("Friendship statuses")


class Friendship(TimeStampedModel):
    from_user = models.ForeignKey(
        "users.AuthUser",
        on_delete=models.CASCADE,
        related_name="from_users",
        verbose_name=_("from users"),
    )
    to_user = models.ForeignKey(
        "users.AuthUser",
        on_delete=models.CASCADE,
        related_name="to_users",
        verbose_name=_("to user"),
    )
    status = models.ForeignKey(
        FriendshipStatus, on_delete=models.PROTECT, verbose_name=_("status")
    )
    # https://django-model-utils.readthedocs.io/en/latest/utilities.html#field-tracker
    since = FieldTracker(fields=["status"])
    weight = models.FloatField(_("weight"), default=1.0, blank=True, null=True)

    # Interactions?

    class Meta:
        ordering = ("modified",)
        verbose_name = _("Friendship")
        verbose_name_plural = _("Friendships")
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"], name="unique-participants"
            )
        ]

    @property
    def is_blocked(self):
        return self.status == FriendshipStatus.objects.blocked()

    def __str__(self):
        return f"Friendship from {self.from_user} to {self.to_user} ({self.status})"
