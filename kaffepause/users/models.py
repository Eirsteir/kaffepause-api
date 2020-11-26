from django.contrib.auth.models import AbstractUser
from neomodel import RelationshipTo, StringProperty, StructuredNode, UniqueIdProperty


class User(StructuredNode):
    uid = (
        UniqueIdProperty()
    )  # https://neomodel.readthedocs.io/en/latest/properties.html#independent-database-property-name
    name = StringProperty(unique_index=True, required=True)
    username = StringProperty(unique_index=True)

    friends = RelationshipTo("User", "FRIEND")
