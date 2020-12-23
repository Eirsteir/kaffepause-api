import factory

from kaffepause.common.bases import NeomodelFactory
from kaffepause.users.models import User


class UserFactory(NeomodelFactory):
    class Meta:
        model = User

    uuid = factory.Faker("uuid4")
    name = factory.Faker("name")
    username = factory.Faker("user_name")
    locale = factory.Faker("locale")
    profile_pic = factory.Faker("url")
