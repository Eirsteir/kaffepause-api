import pytest

from kaffepause.users.forms import UserUpdateForm
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_update_form_clean_username_when_taken(user):
    form = UserUpdateForm(instance=user, data={"username": user.username})

    assert not form.is_valid()


def test_update_form_updates_user(user):
    proto_user = UserFactory.build()

    form = UserUpdateForm(
        instance=user,
        data={
            "name": proto_user.name,
            "username": proto_user.username,
            "locale": proto_user.locale,
            "profile_pic": proto_user.profile_pic,
        },
    )

    assert form.is_valid()
    form.save()
