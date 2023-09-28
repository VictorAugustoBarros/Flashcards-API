"""GraphQL Error."""
from ariadne import format_error
from graphql import GraphQLError


def graphql_format_error(error: GraphQLError, debug: bool = False) -> dict:
    """Classe para controle da exception genérica do GraphQL

    Args:
        error(GraphQLError): Error
        debug(bool): Retorno do erro completo ou mensagem genérica

    Returns:

    """
    if debug:
        return format_error(error, debug)

    formatted = error.formatted
    formatted["message"] = "INTERNAL SERVER ERROR"
    return formatted
