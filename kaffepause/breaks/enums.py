from django.db import models


class InvitationReply(models.TextChoices):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    IGNORED = "ignored"
