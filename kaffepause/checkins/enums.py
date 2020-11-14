from django.db import models


class Intensity(models.TextChoices):
    INTENSELY = "intensly"
    FOCUSED = "focused"
    NOT_SO_FOCUSED = "not so focused"
    UNFOCUSED = "unfocused"