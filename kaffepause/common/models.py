from datetime import datetime

import pytz
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from neomodel import DateTimeProperty, StructuredNode, StructuredRel


from kaffepause.common.enums import BaseStatusEnum


class StatusManager(models.Manager):
    def by_slug(self, status_slug):
        return self.get(slug=status_slug)

    def by_status_enum(self, status_enum: BaseStatusEnum):
        return self.get(slug=status_enum())


class StatusModel(TimeStampedModel):
    name = models.CharField(_("name"), max_length=100)
    verb = models.CharField(_("verb"), max_length=100)
    slug = models.CharField(_("slug"), max_length=100)

    objects = StatusManager()

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name


class TimeStampedRel(StructuredRel):
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))


class TimeStampedNode(StructuredNode):
    __abstract_node__ = True
    created = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
