from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class FriendshipStatusEnum(Enum):
    # name, verb, from_slug, to_slug, slug
    ARE_FRIENDS = (
        "are friends",
        "friends_with",
        "friended_by",
        "friends",
    )
    REQUESTED = (
        "requesting",
        "requested_to",
        "requested_by",
        "requested",
    )
    BLOCKED = (
        "blocking",
        "blocking",
        "blocked",
        "blocked",
    )

    @property
    def verb(self):
        return self.value[0]

    @property
    def from_slug(self):
        return self.value[1]

    @property
    def to_slug(self):
        return self.value[2]

    @property
    def slug(self):
        return self.value[3]
