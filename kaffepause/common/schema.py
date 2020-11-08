from graphene import relay


class UUIDNode(relay.Node):
    """Returns a non-encoded ID from which we can retrieve objects with a UUID field."""

    class Meta:
        name = "UUIDNode"

    @classmethod
    def to_global_id(cls, id):
        return id
