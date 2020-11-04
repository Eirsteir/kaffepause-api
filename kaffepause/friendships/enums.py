from django.db import models
from django.utils.translation import gettext_lazy as _


class FriendshipStatus(models.IntegerChoices):
    # Rename to accepted
    ARE_FRIENDS = 1, _("Are friends")
    REQUESTED = 2, _("Is requested")
    BLOCKED = 3, _("Is blocked")
