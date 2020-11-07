import pytest

from kaffepause.relationships.exceptions import InvalidRelationshipDeletion
from kaffepause.relationships.models import Relationship, RelationshipStatus
from kaffepause.relationships.services import (
    _attempt_to_delete_blocked_relationship,
    _get_or_create_relationship,
    create_relationship,
    delete_relationship,
)
from kaffepause.relationships.test.factories import RelationshipFactory
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_create_relationship(requested_status):
    """Should create and return the created relationship with a default status of 'requested'."""
    from_user = UserFactory()
    to_user = UserFactory()

    relationship = create_relationship(from_user, to_user)

    assert relationship.from_user == from_user
    assert relationship.to_user == to_user
    assert relationship.status == requested_status


def test_create_relationship_with_are_friends_status(are_friends_status):
    """Should create and return the created relationship with the given status."""
    from_user = UserFactory()
    to_user = UserFactory()

    actual_relationship = create_relationship(
        from_user, to_user, status=are_friends_status
    )

    assert actual_relationship.from_user == from_user
    assert actual_relationship.to_user == to_user
    assert actual_relationship.status == are_friends_status


def test_create_relationship_when_relationship_already_exist(
    relationship, requested_status
):
    """Should return the existing relationship."""
    from_user = relationship.from_user
    to_user = relationship.to_user

    actual_relationship = create_relationship(from_user, to_user)

    assert actual_relationship == relationship


def test_create_relationship_when_the_reversed_relationship_already_exist(
    relationship, requested_status
):
    """Should create and return the existing relationship."""
    from_user = relationship.from_user
    to_user = relationship.to_user

    actual_relationship = create_relationship(
        from_user=to_user, to_user=from_user
    )

    assert actual_relationship == relationship


def test_get_or_create_relationship(requested_status):
    """Should create a new relationship with the given users and status when the relationship does not exist."""
    actual_relationship, created = _get_or_create_relationship(
        from_user=UserFactory(), to_user=UserFactory(), status=requested_status
    )

    assert actual_relationship.status == requested_status
    assert created


def test_get_or_create_relationship_when_relationship_exists(relationship):
    """Should return the existing relationship."""
    from_user = relationship.from_user
    to_user = relationship.to_user
    status = relationship.status

    actual_relationship, created = _get_or_create_relationship(
        from_user, to_user, status
    )

    assert actual_relationship == relationship
    assert not created


def test_get_or_create_relationship_when_relationship_exists_with_different_status(
    relationship, are_friends_status
):
    """Should return the existing relationship."""
    from_user = relationship.from_user
    to_user = relationship.to_user

    actual_relationship, created = _get_or_create_relationship(
        from_user, to_user, are_friends_status
    )

    assert actual_relationship == relationship
    assert not created


def test_get_or_create_relationship_when_reverse_relationship_exists(
    relationship,
):
    """Should return the existing relationship."""
    from_user = relationship.to_user
    to_user = relationship.from_user
    status = relationship.status

    actual_relationship, created = _get_or_create_relationship(
        from_user, to_user, status
    )

    assert actual_relationship == relationship
    assert not created


def test_attempt_to_delete_blocked_relationship(blocked_status):
    """Should delete the relationship when the actor is the one blocking."""
    actor = UserFactory()
    relationship = RelationshipFactory(from_user=actor, status=blocked_status)

    _attempt_to_delete_blocked_relationship(actor, relationship)


def test_attempt_to_delete_blocked_relationship_when_actor_is_being_blocked(
    blocked_status,
):
    """Should not delete the relationship when the actor is the one being blocked."""
    actor = UserFactory()
    relationship = RelationshipFactory(to_user=actor, status=blocked_status)

    with pytest.raises(InvalidRelationshipDeletion):
        _attempt_to_delete_blocked_relationship(actor, relationship)


def test_attempt_to_delete_blocked_relationship_when_relationship_status_is_not_blocked(
    requested_status,
):
    """Should not delete the relationship when the status is not 'blocked'."""
    actor = UserFactory()
    relationship = RelationshipFactory(to_user=actor, status=requested_status)

    with pytest.raises(InvalidRelationshipDeletion):
        _attempt_to_delete_blocked_relationship(actor, relationship)


def test_delete_relationship_when_status_is_requested(requested_status):
    """Should delete the relationship when status is 'requested'."""
    actor = UserFactory()
    user = UserFactory()
    relationship = RelationshipFactory(
        from_user=actor, to_user=user, status=requested_status
    )

    delete_relationship(actor, user)

    assert not Relationship.objects.filter(pk=relationship.pk).exists()


def test_delete_relationship_when_status_is_are_friends(are_friends_status):
    """Should delete the relationship when status is 'are_friends'."""
    actor = UserFactory()
    user = UserFactory()
    relationship = RelationshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    delete_relationship(actor, user)

    assert not Relationship.objects.filter(pk=relationship.pk).exists()


def test_delete_relationship_when_status_is_blocked_and_actor_is_blocking(
    blocked_status,
):
    """Should delete the relationship when status is 'blocked' and the actor is the blocker."""
    actor = UserFactory()
    user = UserFactory()
    relationship = RelationshipFactory(
        from_user=actor, to_user=user, status=blocked_status
    )

    delete_relationship(actor, user)

    assert not Relationship.objects.filter(pk=relationship.pk).exists()


def test_delete_relationship_when_status_is_blocked_and_actor_is_being_blocked(
    blocked_status,
):
    """Should not delete the relationship when status is 'blocked' and the actor is being blocked."""
    actor = UserFactory()
    user = UserFactory()
    RelationshipFactory(from_user=user, to_user=actor, status=blocked_status)

    with pytest.raises(InvalidRelationshipDeletion):
        delete_relationship(actor, user)


def test_both_users_can_delete_the_relationship_when_status_is_valid(
    are_friends_status,
):
    """Both users should be able to delete the relationship when status is not 'blocked'"""
    actor = UserFactory()
    user = UserFactory()
    relationship = RelationshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    delete_relationship(actor, user)

    assert not Relationship.objects.filter(pk=relationship.pk).exists()

    relationship = RelationshipFactory(
        from_user=actor, to_user=user, status=are_friends_status
    )

    delete_relationship(actor=user, user=actor)

    assert not Relationship.objects.filter(pk=relationship.pk).exists()
