import graphene
from graphene import relay
from graphene_django.utils import camelize


class CountingNodeConnection(relay.Connection):
    """Connection to include a node and edges count."""

    class Meta:
        abstract = True

    count = graphene.Int()
    edge_count = graphene.Int()

    # TODO: fix this, returns count of all nodes
    def resolve_count(root, info, **kwargs):
        return len(root.iterable)

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class OutputErrorType(graphene.Scalar):
    class Meta:
        description = """
    Errors messages and codes mapped to
    fields or non fields errors.
    Example:
    {
        field_name: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        other_field: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ],
        nonFieldErrors: [
            {
                "message": "error message",
                "code": "error_code"
            }
        ]
    }
    """

    @staticmethod
    def serialize(errors):
        if isinstance(errors, dict):
            if errors.get("__all__", False):
                errors["non_field_errors"] = errors.pop("__all__")
            return camelize(errors)
        elif isinstance(errors, list):
            return {"nonFieldErrors": errors}
        raise ValueError("`errors` must be list or dict!")
