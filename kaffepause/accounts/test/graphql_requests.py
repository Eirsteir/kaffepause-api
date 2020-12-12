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

DELETE_ACCOUNT_MUTATION = """
    mutation deleteAccount($password: String!) {
        deleteAccount(password: $password) {
            success
            errors
        }
    }
"""

MY_ACCOUNT_QUERY = """
    query myAccount {
      myAccount {
        uuid
        email
        secondaryEmail
        verified
        archived
      }
    }
"""
