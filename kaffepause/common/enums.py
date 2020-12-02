from enum import Enum


class BaseStatusEnum(Enum):
    """
    Mirrors :class:`StatusModel` in which subclasses have to define
    member variables in the form of a tuple (verb, slug).
    The name member variable is inferred from the name of the attribute.
    """

    def __call__(self, *args, **kwargs):
        """Avoid having to call `.slug` in every query where slug is often the most relevant lookup field."""
        return self.slug

    @property
    def verb(self):
        return self.value[0]

    @property
    def slug(self):
        return self.value[1]


class Node(Enum):
    USER = "User"
    BREAK = "Break"
    BREAK_INVITATION = "BreakInvitation"
