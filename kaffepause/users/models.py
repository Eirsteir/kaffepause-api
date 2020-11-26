from django.contrib.auth.models import AbstractUser
from neomodel import (
    IntegerProperty,
    RelationshipTo,
    StringProperty,
    StructuredNode,
    UniqueIdProperty,
)


class User(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    friends = RelationshipTo("User", "FRIEND")
