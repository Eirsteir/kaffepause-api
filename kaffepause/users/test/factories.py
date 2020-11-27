import factory

from kaffepause.users.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    name = factory.Faker("name")

    friends = factory.SubFactory("kaffepause.users.test.factories.UserFactory")
