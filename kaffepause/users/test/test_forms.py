import pytest

from kaffepause.users.forms import UserUpdateForm
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_update_form_clean_username_when_taken(user):
    form = UserUpdateForm(instance=user, data={"username": user.username})

    assert not form.is_valid()


def test_update_form_only_updates_fields_passed(user):
    proto_user = UserFactory.build()
    expected = (user.locale, user.profile_pic, proto_user.username, proto_user.name)
    print(user.profile_pic)

    form = UserUpdateForm(
        instance=user,
        data={
            "username": proto_user.username,
            "name": proto_user.name,
        },
    )
    user2 = form.save()
    print(user2)
    actual = (user.locale, user.profile_pic, user.username, user.name)

    assert form.is_valid()
    assert actual == expected
