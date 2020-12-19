import graphene
from graphene import relay
from graphene_django.utils import camelize


class CountableConnection(relay.Connection):
    """Connection to include a total edges count."""

    class Meta:
        abstract = True

    count = graphene.Int()
    total_count = graphene.Int()

    def resolve_count(root, info, **kwargs):
        return len(root.edges)

    def resolve_total_count(root, info, **kwargs):
        return len(root.iterable)


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
