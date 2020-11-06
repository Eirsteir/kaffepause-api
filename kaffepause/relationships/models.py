from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from kaffepause.relationships.enums import RelationshipStatusEnum

User = get_user_model()


class RelationshipStatusManager(models.Manager):
    def requested(self):
        return self.get(slug=RelationshipStatusEnum.REQUESTED.slug)

    def blocked(self):
        return self.get(slug=RelationshipStatusEnum.BLOCKED.slug)

    def friends(self):
        return self.get(slug=RelationshipStatusEnum.ARE_FRIENDS.slug)

    def by_slug(self, status_slug):
        return self.get(slug=status_slug)

    def by_status_enum(self, status_enum: RelationshipStatusEnum):
        return self.get(slug=status_enum.slug)


class RelationshipStatus(models.Model):
    name = models.CharField(_("name"), max_length=100)
    verb = models.CharField(_("verb"), max_length=100)
    slug = models.CharField(
        _("slug"),
        max_length=100,
        help_text=_("When a mutual relationship exists, i.e. 'friends', 'requested'"),
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


class Relationship(models.Model):
    from_user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="from_users",
        verbose_name=_("from users"),
    )
    to_user = models.ForeignKey(
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
            "from_user",
            "to_user",
        )
        ordering = ("created",)
        verbose_name = _("Friendship")
        verbose_name_plural = _("Friendship")

    def __str__(self):
        return f"Relationship from {self.from_user} to {self.to_user} ({self.status})"
