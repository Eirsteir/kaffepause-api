from django.db import models

from kaffepause.common.enums import BaseStatusEnum


class Intensity(models.TextChoices):
    INTENSELY = "intensly"
    FOCUSED = "focused"
    NOT_SO_FOCUSED = "not so focused"
    UNFOCUSED = "unfocused"


class CheckInStatus(BaseStatusEnum):
    READING = ("is reading", "reading")
    RELAXING = ("is relaxing", "relaxing")
    READY_FOR_A_BREAK = ("is ready for a break", "ready_for_a_break")
