import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from neomodel import (
    IntegerProperty,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "id"

    def __str__(self):
        return self.email


class Person(StructuredNode):
    id = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    friends = RelationshipTo("Person", "FRIEND")
