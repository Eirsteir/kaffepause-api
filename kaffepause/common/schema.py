import graphene
from graphene import Connection, relay


class UUIDNode(relay.Node):
    """Returns a non-encoded ID from which we can retrieve objects with a UUID field."""

    class Meta:
        name = "UUIDNode"

    @classmethod
    def to_global_id(cls, type, id):
        return id


class CountingNodeConnection(Connection):
    class Meta:
        abstract = True

    count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)
