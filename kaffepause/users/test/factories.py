import factory

from kaffepause.common.bases import NeomodelFactory
from kaffepause.users.models import User


class UserFactory(NeomodelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    name = factory.Faker("name")
