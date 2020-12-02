import pytest

from kaffepause.breaks.models import Break, BreakInvitation
from kaffepause.breaks.test.factories import BreakFactory, BreakInvitationFactory
from kaffepause.users.models import User
from kaffepause.users.test.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture(autouse=True)
def break_() -> Break:
    break_ = BreakFactory()
    break_.participants.connect(UserFactory())
    return break_


@pytest.fixture(autouse=True)
def break_invitation(break_) -> BreakInvitation:
    break_invitation = BreakInvitationFactory()
    break_invitation.subject.connect(break_)
    return break_invitation
