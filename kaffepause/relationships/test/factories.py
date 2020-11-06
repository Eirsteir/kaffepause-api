from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from kaffepause.relationships.enums import RelationshipStatusEnum
from kaffepause.relationships.models import Relationship, RelationshipStatus
from kaffepause.users.test.factories import UserFactory


class RelationshipStatusFactory(DjangoModelFactory):
    """Requires slug to be of type :class:`RelationshipStatusEnum`:"""

    class Meta:
        model = RelationshipStatus
        django_get_or_create = ("slug",)

    name = LazyAttribute(lambda o: o.slug.name)
    verb = LazyAttribute(lambda o: o.slug.label)
    slug = LazyAttribute(lambda o: o.slug.value)


class RelationshipFactory(DjangoModelFactory):
    """Status defaults to requested."""

    class Meta:
        model = Relationship

    from_user = SubFactory(UserFactory)
    to_user = SubFactory(UserFactory)
    status = SubFactory(
        RelationshipStatusFactory, slug=RelationshipStatusEnum.REQUESTED
    )
