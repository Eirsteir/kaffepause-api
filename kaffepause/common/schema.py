import graphene
from graphene import relay

from kaffepause.common.types import OutputErrorType


class UUIDNode(relay.Node):
    """Returns a non-encoded ID from which we can retrieve objects with a UUID field."""

    class Meta:
        name = "UUIDNode"

    @classmethod
    def to_global_id(cls, type, id):
        return id


class Output:
    """
    A class to all public classes extend to
    standardize the output
    """

    success = graphene.Boolean(default_value=True)
    errors = graphene.Field(OutputErrorType)
