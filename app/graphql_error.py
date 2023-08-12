from graphql import GraphQLError
from ariadne import format_error


def graphql_format_error(error: GraphQLError, debug: bool = False) -> dict:
    if debug:
        return format_error(error, debug)

    formatted = error.formatted
    formatted["message"] = "INTERNAL SERVER ERROR"
    return formatted
