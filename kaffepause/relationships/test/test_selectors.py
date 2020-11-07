import pytest

from kaffepause.relationships.models import Relationship
from kaffepause.relationships.selectors import (
    get_friends,
    get_incoming_blocks,
    get_incoming_relationships_for,
    get_incoming_requests,
    get_outgoing_blocks,
    get_outgoing_relationships_for,
    get_outgoing_requests,
    get_relationships_for,
    get_single_relationship,
    relationship_exists,
)
from kaffepause.relationships.test.factories import RelationshipFactory
from kaffepause.users.test.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_get_relationships_for(user, are_friends_status, requested_status):
    """Should return exclusively users who are in an accepted relationship with the given user."""
    outgoing_accepted = RelationshipFactory(
        from_user=user, status=are_friends_status
    )
    incoming_accepted = RelationshipFactory(
        to_user=user, status=are_friends_status
    )

    # Leave out other relationships
    RelationshipFactory(to_user=user)

    friends = get_relationships_for(user, are_friends_status)

    assert friends.count() == 2
    assert friends.filter(id=outgoing_accepted.to_user.id).exists()
    assert friends.filter(id=incoming_accepted.from_user.id).exists()


def test_get_relationships_for_when_user_has_no_relationships(
    user, are_friends_status
):
    """Should return no users when user has no relationships."""
    friends = get_relationships_for(user, are_friends_status)

    assert not friends.count()


def test_get_incoming_relationships_for(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who have created a relationship to the given user."""
    incoming_request = RelationshipFactory(to_user=user)

    # Leave out other relationships
    RelationshipFactory.create(from_user=user)
    RelationshipFactory.create(to_user=user, status=are_friends_status)
    RelationshipFactory.create(from_user=user, status=blocked_status)

    friends = get_incoming_relationships_for(user, requested_status)

    assert friends.count() == 1
    assert friends.filter(id=incoming_request.from_user.id).exists()


def test_get_outgoing_relationships_for(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who the given user has created a relationship to."""
    outgoing_request = RelationshipFactory(from_user=user)

    # Leave out other relationships
    RelationshipFactory.create(to_user=user)
    RelationshipFactory.create(to_user=user, status=are_friends_status)
    RelationshipFactory.create(from_user=user, status=blocked_status)

    friends = get_outgoing_relationships_for(user, requested_status)

    assert friends.count() == 1
    assert friends.filter(id=outgoing_request.to_user.id).exists()


def test_relationship_exists_excluding_status_asymmetrical(relationship):
    """Should return true if a relationship with the respective users exists."""
    from_user = relationship.from_user
    to_user = relationship.to_user

    assert relationship_exists(from_user, to_user)


def test_relationship_exists_excluding_status_asymmetrical_reversed(
    relationship,
):
    """Should return true if a relationship with the respective users exists."""
    from_user = relationship.to_user
    to_user = relationship.from_user

    assert not relationship_exists(from_user, to_user)


def test_relationship_exists_excluding_status_asymmetrical_when_it_does_not_exist():
    """Should return false if an asymmetrical relationship with the respective users does not exist."""

    assert not relationship_exists(
        from_user=UserFactory(), to_user=UserFactory()
    )


def test_relationship_exists_including_status_asymmetrical(relationship):
    """Should return true if an asymmetrical relationship with the respective users and status exists."""
    from_user = relationship.from_user
    to_user = relationship.to_user
    status = relationship.status

    assert relationship_exists(from_user, to_user, status)


def test_relationship_exists_including_status_asymmetrical_reversed(
    relationship,
):
    """Should return false if an asymmetrical reversed relationship with the respective users and status does not exists."""
    from_user = relationship.to_user
    to_user = relationship.from_user
    status = relationship.status

    assert not relationship_exists(from_user, to_user, status)


def test_relationship_exists_including_status__asymmetrical_when_it_does_not_exist(
    requested_status,
):
    """Should return false if an asymmetrical relationship with the respective users and status does not exist."""

    assert not relationship_exists(
        from_user=UserFactory(), to_user=UserFactory(), status=requested_status
    )


def test_relationship_exists_excluding_status_symmetrical(relationship):
    """Should return true if a symmetrical relationship with the respective users exists."""
    from_user = relationship.from_user
    to_user = relationship.to_user

    assert relationship_exists(from_user, to_user, symmetrical=True)


def test_relationship_exists_excluding_status_symmetrical_reversed(
    relationship,
):
    """Should return true if a symmetrical relationship with the respective users exists."""
    from_user = relationship.to_user
    to_user = relationship.from_user

    assert relationship_exists(from_user, to_user, symmetrical=True)


def test_relationship_exists_excluding_status_symmetrical_when_it_does_not_exist():
    """Should return false if a symmetrical relationship with the respective users does not exist."""

    assert not relationship_exists(
        from_user=UserFactory(), to_user=UserFactory(), symmetrical=True
    )


def test_relationship_exists_including_status_symmetrical(relationship):
    """Should return true if a symmetrical relationship with the respective users and status exists."""
    from_user = relationship.from_user
    to_user = relationship.to_user
    status = relationship.status

    assert relationship_exists(
        from_user, to_user, status=status, symmetrical=True
    )


def test_relationship_exists_including_status_symmetrical_reversed(
    relationship,
):
    """Should return true if a symmetrical relationship with the respective users and status exists."""
    from_user = relationship.from_user
    to_user = relationship.to_user
    status = relationship.status

    assert relationship_exists(
        from_user, to_user, status=status, symmetrical=True
    )


def test_relationship_exists_including_status__symmetrical_when_it_does_not_exist(
    requested_status,
):
    """Should return false if a symmetrical relationship with the respective users and status does not exist."""

    assert not relationship_exists(
        from_user=UserFactory(),
        to_user=UserFactory(),
        status=requested_status,
        symmetrical=True,
    )


def test_get_friends(user, are_friends_status, requested_status):
    """Should return exclusively users who are in an accepted relationship with the given user."""
    outgoing_accepted = RelationshipFactory(
        from_user=user, status=are_friends_status
    )
    incoming_accepted = RelationshipFactory(
        to_user=user, status=are_friends_status
    )

    # Leave out other relationships
    RelationshipFactory(to_user=user)

    friends = get_friends(user)

    assert friends.count() == 2
    assert friends.filter(id=outgoing_accepted.to_user.id).exists()
    assert friends.filter(id=incoming_accepted.from_user.id).exists()


def test_get_incoming_requests(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who have created a requested relationship to the given user."""
    incoming_request = RelationshipFactory(to_user=user)

    # Leave out other relationships
    RelationshipFactory.create(from_user=user)
    RelationshipFactory.create(to_user=user, status=are_friends_status)
    RelationshipFactory.create(from_user=user, status=blocked_status)

    friends = get_incoming_requests(user)

    assert friends.count() == 1
    assert friends.filter(id=incoming_request.from_user.id).exists()


def test_get_outgoing_requests(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who the given user has created a requested relationship to."""
    outgoing_request = RelationshipFactory(from_user=user)

    # Leave out other relationships
    RelationshipFactory.create(to_user=user)
    RelationshipFactory.create(to_user=user, status=are_friends_status)
    RelationshipFactory.create(from_user=user, status=blocked_status)

    friends = get_outgoing_requests(user)

    assert friends.count() == 1
    assert friends.filter(id=outgoing_request.to_user.id).exists()


def test_get_incoming_blocks(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who have created a blocked relationship to the given user."""
    incoming_block = RelationshipFactory(to_user=user, status=blocked_status)

    # Leave out other relationships
    RelationshipFactory.create(from_user=user)
    RelationshipFactory.create(to_user=user, status=are_friends_status)
    RelationshipFactory.create(from_user=user)

    friends = get_incoming_blocks(user)

    assert friends.count() == 1
    assert friends.filter(id=incoming_block.from_user.id).exists()


def test_get_outgoing_blocks(
    user, are_friends_status, blocked_status, requested_status
):
    """Should return all users who the given user has created a blocked relationship to."""
    outgoing_block = RelationshipFactory(from_user=user, status=blocked_status)

    # Leave out other relationships
    RelationshipFactory.create(to_user=user)
    RelationshipFactory.create(to_user=user, status=are_friends_status)
    RelationshipFactory.create(from_user=user)

    friends = get_outgoing_blocks(user)

    assert friends.count() == 1
    assert friends.filter(id=outgoing_block.to_user.id).exists()


def test_get_single_relationship_excluding_status(relationship):
    """Should return the relationship if a relationship with the respective users exists."""
    from_user = relationship.from_user
    to_user = relationship.to_user

    actual_relationship = get_single_relationship(from_user, to_user)

    assert actual_relationship == relationship


def test_get_single_relationship_excluding_status_reversed(
    relationship,
):
    """Should return the relationship if a reversed relationship with the respective users exists."""
    from_user = relationship.to_user
    to_user = relationship.from_user

    actual_relationship = get_single_relationship(from_user, to_user)

    assert actual_relationship == relationship


def test_get_single_relationship_excluding_status_when_it_does_not_exist():
    """Should raise an exception if a relationship with the respective users does not exist."""
    with pytest.raises(Relationship.DoesNotExist):
        get_single_relationship(from_user=UserFactory(), to_user=UserFactory())


def test_get_single_relationship_including_status(relationship):
    """Should return  the relationship if a relationship with the respective users and status exists."""
    from_user = relationship.from_user
    to_user = relationship.to_user
    status = relationship.status

    actual_relationship = get_single_relationship(from_user, to_user, status)

    assert actual_relationship == relationship


def test_get_single_relationship_including_status_reversed(
    relationship,
):
    """Should return nothing if a reversed relationship with the respective users and status does not exists."""
    from_user = relationship.to_user
    to_user = relationship.from_user
    status = relationship.status

    actual_relationship = get_single_relationship(from_user, to_user, status)

    assert actual_relationship == relationship


def test_get_single_relationship_including_status__when_it_does_not_exist(
    requested_status,
):
    """Should raise an exception if a relationship with the respective users and status does not exist."""
    with pytest.raises(Relationship.DoesNotExist):
        get_single_relationship(
            from_user=UserFactory(),
            to_user=UserFactory(),
            status=requested_status,
        )
