from django.contrib.auth import get_user_model
from django.db import models

from kaffepause.common.models import BaseModel

from .enums import FriendshipStatus

User = get_user_model()


class Friendship(BaseModel):

    requester = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_requested_by_user"
    )
    addressee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_addressed_at_user"
    )
    status = models.IntegerField(
        choices=FriendshipStatus.choices, default=FriendshipStatus.REQUESTED
    )

    # A score based on interactions, invitations? Read only
    score = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["requester", "addressee"]
        index_together = ["requester", "addressee"]
        ordering = ["score"]

    def __str__(self):
        if self.status == FriendshipStatus.ARE_FRIENDS:
            return f"{self.requester} and {self.addressee} {self.get_status_display().lower()}"
        elif self.status == FriendshipStatus.REQUESTED:
            return f"{self.requester}'s friendship to {self.addressee} {self.get_status_display().lower()}"
        return f"{self.requester}'s friendship to {self.addressee} {self.get_status_display().lower()}"
