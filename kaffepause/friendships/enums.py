from enum import Enum

from kaffepause.common.enums import BaseStatusEnum


class BaseFriendshipStatusEnum(BaseStatusEnum):
    """
    Mirrors :class:`FriendshipStatus` in which subclasses have to define
    member variables in the form of a tuple (verb, slug, from_slug, to_slug).
    The name member variable is inferred from the name of the attribute.
    """

    @property
    def from_slug(self):
        return self.value[2]

    @property
    def to_slug(self):
        return self.value[3]

    @classmethod
    def from_name(cls, name):
        return cls[name]


class DefaultFriendshipStatus(BaseFriendshipStatusEnum):
    ARE_FRIENDS = (
        "are friends",
        "friends",
        "friends_with",
        "friended_by",
    )
    REQUESTED = (
        "requesting",
        "requested",
        "requested_to",
        "requested_by",
    )
    BLOCKED = (
        "blocking",
        "blocked",
        "blocking",
        "blocked",
    )


# TODO: Misleading name?
class NonFriendsFriendshipStatus(BaseFriendshipStatusEnum):
    CAN_REQUEST = (
        "Can request",
        "can_request_to",
        "can_be_requested_by",
        "can_request",
    )
    CANNOT_REQUEST = (
        "Cannot request",
        "cannot_request_to",
        "cannot_be_requested_by",
        "cannot_request",
    )
