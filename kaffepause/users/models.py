import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    friends = models.ManyToManyField(
        "self",
        through="friendships.Friendship",
        symmetrical=False,
        related_name="related_to+",  # The reverse friendship should not be exposed
    )

    def __str__(self):
        return self.username
