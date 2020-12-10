import pytest

from kaffepause.statusupdates.enums import StatusUpdateType
from kaffepause.statusupdates.services import update_status
from kaffepause.statusupdates.test.factories import StatusUpdateFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_with_status(user):
    user.current_status.connect(StatusUpdateFactory())
    return user


def test_update_status_when_user_has_no_current_status_sets_status(user):
    """Should set the users current status to that of the given type."""
    new_status_type = StatusUpdateType.FOCUSMODE

    actual_status = update_status(actor=user, status_type=new_status_type)

    assert user.current_status.is_connected(actual_status)
    assert actual_status.status_type == new_status_type.name


def test_update_status_when_user_has_current_status_replaces_status(user_with_status):
    """Should replace the users current status to that of the given type."""
    new_status_type = StatusUpdateType.FOCUSMODE
    old_status_type = user_with_status.current_status.single().status_type

    update_status(actor=user_with_status, status_type=new_status_type)

    actual_status = user_with_status.current_status.single()

    assert actual_status.status_type == new_status_type.name
    assert old_status_type != new_status_type


def test_update_status_when_user_has_current_status_sets_old_to_previous(
    user_with_status,
):
    """Should set the old status to 'previous' of the new status."""
    new_status_type = StatusUpdateType.FOCUSMODE
    old_status = user_with_status.current_status.single()

    update_status(actor=user_with_status, status_type=new_status_type)

    actual_status = user_with_status.current_status.single()

    assert actual_status.status_type == new_status_type.name
    assert actual_status.previous.single() == old_status
