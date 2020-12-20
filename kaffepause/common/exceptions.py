from graphql import GraphQLError


class DefaultError(GraphQLError):
    default_message = None

    def __init__(self, message=default_message):
        super().__init__(message)
