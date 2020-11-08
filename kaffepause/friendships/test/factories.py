from typing import Any, Sequence

from factory import LazyAttribute, SubFactory, fuzzy, post_generation
from factory.django import DjangoModelFactory

from kaffepause.friendships.enums import (
    BaseFriendshipStatusEnum,
    DefaultFriendshipStatus,
)
from kaffepause.friendships.models import Friendship, FriendshipStatus
from kaffepause.users.test.factories import UserFactory


class FriendshipStatusFactory(DjangoModelFactory):
    """Requires slug to be of type :class:`DefaultFriendshipStatus`:"""

    class Meta:
        model = FriendshipStatus
        django_get_or_create = ("name",)

    name = fuzzy.FuzzyChoice(DefaultFriendshipStatus, getter=lambda n: n.name)

    @classmethod
    def from_enum(cls, enum: BaseFriendshipStatusEnum) -> FriendshipStatus:
        instance = cls.build(
            name=enum.name,
            verb=enum.verb,
            from_slug=enum.from_slug,
            to_slug=enum.to_slug,
            slug=enum.slug,
        )

        if FriendshipStatus.objects.filter(name=instance.name).exists():
            return FriendshipStatus.objects.get(name=instance.name)

        instance.save()
        return instance


class FriendshipFactory(DjangoModelFactory):
    """Status defaults to requested."""

    class Meta:
        model = Friendship

    from_user = SubFactory(UserFactory)
    to_user = SubFactory(UserFactory)
    status = SubFactory(FriendshipStatusFactory)
