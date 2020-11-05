from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class RelationshipStatusManager(models.Manager):
    def requesting(self):
        return self.get(from_slug="requesting")

    def requested(self):
        return self.get(to_slug="requested")

    def blocking(self):
        return self.get(from_slug="blocking")

    def are_friends(self):
        return self.get(symmetrical_slug="are_friends")

    def by_slug(self, status_slug):
        return self.get(
            models.Q(from_slug=status_slug)
            | models.Q(to_slug=status_slug)
            | models.Q(symmetrical_slug=status_slug)
        )


class RelationshipStatus(models.Model):
    name = models.CharField(_("name"), max_length=100)
    verb = models.CharField(_("verb"), max_length=100)
    from_slug = models.CharField(
        _("from slug"),
        max_length=100,
        help_text=_("Denote the relationship from the user, i.e. 'requesting'"),
    )
    to_slug = models.CharField(
        _("to slug"),
        max_length=100,
        help_text=_("Denote the relationship to the user, i.e. 'requested'"),
    )
    symmetrical_slug = models.CharField(
        _("symmetrical slug"),
        max_length=100,
        help_text=_("When a mutual relationship exists, i.e. 'friends'"),
    )
    login_required = models.BooleanField(
        _("login required"),
        default=False,
        help_text=_("Users must be logged in to see these relationships"),
    )
    private = models.BooleanField(
        _("private"),
        default=False,
        help_text=_("Only the user who owns these relationships can see them"),
    )

    objects = RelationshipStatusManager()

    class Meta:
        ordering = ("name",)
        verbose_name = _("Relationship status")
        verbose_name_plural = _("Relationship statuses")

    def __str__(self):
        return self.name


class Friendship(models.Model):
    requester = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="from_users",
        verbose_name=_("from users"),
    )
    addressee = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="to_users",
        verbose_name=_("to user"),
    )
    status = models.ForeignKey(
        RelationshipStatus, on_delete=models.PROTECT, verbose_name=_("status")
    )
    created = models.DateTimeField(_("created"), auto_now_add=True)
    weight = models.FloatField(_("weight"), default=1.0, blank=True, null=True)

    class Meta:
        unique_together = (
            "requester",
            "addressee",
        )
        ordering = ("created",)
        verbose_name = _("Friendship")
        verbose_name_plural = _("Friendship")

    def __str__(self):
        return f"Relationship from {self.requester} to {self.addressee}"
