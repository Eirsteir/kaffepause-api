from enum import Enum


class BaseFriendshipStatusEnum(Enum):
    """
    Mirrors :class:`FriendshipStatus` in which subclasses have to define
    member variables in the form of a tuple (verb, from_slug, to_slug, slug).
    The name member variable is inferred from the name of the attribute.
    """

    @property
    def verb(self):
        return self.value[0]

    @property
    def from_slug(self):
        return self.value[1]

    @property
    def to_slug(self):
        return self.value[2]

    @property
    def slug(self):
        return self.value[3]

    @classmethod
    def from_name(cls, name):
        return cls[name]


class DefaultFriendshipStatus(BaseFriendshipStatusEnum):
    ARE_FRIENDS = (
        "are friends",
        "friends_with",
        "friended_by",
        "friends",
    )
    REQUESTED = (
        "requesting",
        "requested_to",
        "requested_by",
        "requested",
    )
    BLOCKED = (
        "blocking",
        "blocking",
        "blocked",
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
