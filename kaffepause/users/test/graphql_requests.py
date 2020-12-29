"""Queries and mutations used by the test suite."""

UPDATE_PROFILE_MUTATION = """
    mutation updateProfile(
        $name: String!,
        $username: String!,
        $locale: String!,
        $profilePic: String!
    ) {
      updateProfile(
        name: $name,
        username: $username,
        locale: $locale,
        profilePic: $profilePic
    ) {
        success
        errors
        user {
          uuid
          name
          username
          locale
          profilePic
        }
      }
    }
"""

SEARCH_QUERY = """
    query searchUsers($query: String!) {
      searchUsers(query: $query) {
        count
        edges {
            node {
                uuid
                username
                name
            }
        }
      }
    }
"""
