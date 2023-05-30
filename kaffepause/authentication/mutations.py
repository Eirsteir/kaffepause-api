import graphene
from graphql import GraphQLError

from kaffepause.authentication.backend import JSONWebTokenBackend, Neo4jSessionBackend
from kaffepause.authentication.jwt import create_access_token
import kaffepause.users.types


class ObtainJSONWebToken(graphene.Mutation):
    """
    Mutation to obtain a JSON Web Token
    """
    class Arguments:
        session_token = graphene.String(required=True)

    access_token = graphene.String()
    user = graphene.Field(lambda: kaffepause.users.types.UserNode)

    def mutate(self, info, session_token):
        """
        Mutation to obtain a JSON Web Token
        """
        user = Neo4jSessionBackend().authenticate(session_token=session_token)

        if user is None:
            raise GraphQLError('Invalid credentials')

        access_token = create_access_token(user)

        return ObtainJSONWebToken(access_token=access_token, user=user)


class SocialAuthJWT(graphene.Mutation):
    """
    Mutation to authenticate a user with a social media provider
    """
    class Arguments:
        provider = graphene.String(required=True)
        access_token = graphene.String(required=True)

    access_token = graphene.String()
    user = graphene.Field(lambda: kaffepause.users.types.UserNode)

    def mutate(self, info, provider, access_token):
        """
        Mutation to obtain a JSON Web Token
        """
        user = Neo4jSessionBackend().authenticate(provider=provider, access_token=access_token)

        if user is None:
            raise GraphQLError('Invalid credentials')

        access_token = create_access_token(user)

        return ObtainJSONWebToken(access_token=access_token, user=user)
