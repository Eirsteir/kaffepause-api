from django.db import models
from django.utils.translation import gettext_lazy as _


class RelationshipStatusEnum(models.TextChoices):
    # slug, verb
    ARE_FRIENDS = "are_friends", _("are friends")
    REQUESTED = "requested", _("is requested")
    BLOCKED = "blocked", _("is blocked")

    @property
    def slug(self):
        return self.value

    @property
    def verb(self):
        return self.label
