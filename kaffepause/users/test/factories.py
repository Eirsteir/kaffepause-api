from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory
from graphql_auth.models import UserStatus


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )

        # Special case where factory is built as a dictionary
        if isinstance(self, dict):
            self["password"] = password
            return

        self.set_password(password)


class UserStatusFactory(DjangoModelFactory):
    class Meta:
        model = UserStatus

    user = SubFactory(UserFactory)
