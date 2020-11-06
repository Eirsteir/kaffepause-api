from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from kaffepause.relationships.models import Relationship, RelationshipStatus
from kaffepause.users.test.factories import UserFactory


class RelationshipStatusFactory(DjangoModelFactory):
    class Meta:
        model = RelationshipStatus
        django_get_or_create = ("slug",)

    name = LazyAttribute(lambda o: o.slug.name)
    verb = LazyAttribute(lambda o: o.slug.label)
    slug = LazyAttribute(lambda o: o.slug.value)


class RelationshipFactory(DjangoModelFactory):
    class Meta:
        model = Relationship

    from_user = SubFactory(UserFactory)
    to_user = SubFactory(UserFactory)
    status = SubFactory(RelationshipStatusFactory)
