import pytest

from kaffepause.accounts.forms import AccountCreationForm
from kaffepause.accounts.test.factories import AccountFactory

pytestmark = pytest.mark.django_db


class TestAccountCreationForm:
    def test_clean_username(self):
        # A user with proto_user params does not exist yet.
        proto_user = AccountFactory.build()

        form = AccountCreationForm(
            {
                "email": proto_user.email,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )

        assert form.is_valid()
        assert form.cleaned_data.get("email") == proto_user.email

        # Creating a user.
        form.save()

        # The user with proto_user params already exists,
        # hence cannot be created.
        form = AccountCreationForm(
            {
                "email": proto_user.email,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
