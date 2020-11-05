from factory import SubFactory
from factory.django import DjangoModelFactory

from kaffepause.friendships.models import Friendship, RelationshipStatus
from kaffepause.users.test.factories import UserFactory


class RelationshipStatusFactory(DjangoModelFactory):
    class Meta:
        model = RelationshipStatus


class FriendshipFactory(DjangoModelFactory):
    class Meta:
        model = Friendship

    requester = SubFactory(UserFactory)
    addressee = SubFactory(UserFactory)
    status = SubFactory(RelationshipStatusFactory)
