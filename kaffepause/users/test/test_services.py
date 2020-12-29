import pytest
from django.core.exceptions import ValidationError

from kaffepause.users.services import update_profile
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_update_profile_updates_profile(user):
    """Should update given fields on the user object."""
    proto_user = UserFactory.build()

    data = {
        "name": proto_user.name,
        "username": proto_user.username,
        "locale": proto_user.locale,
        "profile_pic": proto_user.profile_pic,
    }

    updated_user = update_profile(user=user, data=data)

    assert updated_user.name == proto_user.name
    assert updated_user.username == proto_user.username
    assert updated_user.locale == proto_user.locale
    assert updated_user.profile_pic == proto_user.profile_pic


def test_update_profile_when_form_invalid_fails(user):
    """The update should fail when the form is invalid."""
    with pytest.raises(ValidationError):
        update_profile(user=user, data={})


def test_update_profile_when_username_already_in_use_by_updater(user):
    """Should still update other fields if username is in use by the one performing the update."""
    proto_user = UserFactory.build()

    data = {
        "username": user.username,
        "name": proto_user.name,
        "locale": proto_user.locale,
        "profile_pic": proto_user.profile_pic,
    }

    updated_user = update_profile(user=user, data=data)

    assert updated_user.username == user.username
    assert updated_user.name == proto_user.name
    assert updated_user.locale == proto_user.locale
    assert updated_user.profile_pic == proto_user.profile_pic
