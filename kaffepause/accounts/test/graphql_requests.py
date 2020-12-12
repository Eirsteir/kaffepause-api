"""Queries and mutations used by the test suite."""

REGISTER_MUTATION = """
    mutation register($name: String!,
                      $email: String!,
                      $password1: String!,
                      $password2: String!) {
        register(name: $name,
                 email: $email,
                 password1: $password1,
                 password2: $password2) {
            success
            errors
            refreshToken
            token
        }
    }
"""
