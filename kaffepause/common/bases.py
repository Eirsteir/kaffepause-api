import factory
import graphene
from factory.base import FactoryMetaClass
from graphene import relay
from graphql_auth.decorators import verification_required

from kaffepause.common.types import OutputErrorType
from kaffepause.users.models import User


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

    success = graphene.Boolean(default_value=False)
    errors = graphene.Field(OutputErrorType)


class VerificationRequiredMixin:
    """
    All mutations which requires user to be verified should extend this class.
    """

    @classmethod
    @verification_required
    def mutate(cls, root, info, **input):
        return cls.resolve_mutation(root, info, **input)


class Mutation(VerificationRequiredMixin, Output, graphene.Mutation):
    pass


class NeomodelGraphQLMixin:
    @classmethod
    def get_current_user(cls, info):
        current_user_account = info.context.user
        current_user = User.nodes.get(uid=current_user_account.id)
        return current_user


class NeomodelFactoryMetaClass(FactoryMetaClass):
    """Factory metaclass for handling neomodel StructuredNode classes."""

    def __call__(cls, **kwargs):
        """
        Override the default Factory() syntax to call the default strategy.
        Returns an instance of the associated class.

        Save the StructuredNode instance if the strategy is create.
        """
        instance = super().__call__(**kwargs)
        if cls._meta.strategy == factory.enums.CREATE_STRATEGY:
            instance.save()

        return instance


class NeomodelFactory(factory.Factory, metaclass=NeomodelFactoryMetaClass):
    pass
