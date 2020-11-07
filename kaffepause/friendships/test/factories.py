from factory import LazyAttribute, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from kaffepause.friendships.enums import FriendshipStatusEnum
from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.users.test.factories import UserFactory


class FriendshipStatusFactory(DjangoModelFactory):
    """Requires slug to be of type :class:`FriendshipStatusEnum`:"""

    class Meta:
        model = FriendshipStatus
        django_get_or_create = ("slug",)

    name = fuzzy.FuzzyChoice(FriendshipStatusEnum)
    verb = LazyAttribute(lambda o: o.name.verb)
    from_slug = LazyAttribute(lambda o: o.name.from_slug)
    to_slug = LazyAttribute(lambda o: o.name.to_slug)
    slug = LazyAttribute(lambda o: o.name.slug)


class FriendshipFactory(DjangoModelFactory):
    """Status defaults to requested."""

    class Meta:
        model = Friendship

    from_user = SubFactory(UserFactory)
    to_user = SubFactory(UserFactory)
    status = SubFactory(FriendshipStatusFactory)
