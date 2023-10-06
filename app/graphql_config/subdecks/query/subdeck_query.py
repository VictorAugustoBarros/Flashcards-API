"""Subdeck Query GraphQL."""
from ariadne import QueryType

from app.connections.mysql import MySQLDB
from app.graphql_config.models.response import Response
from app.graphql_config.models.subdeck_response import (
    SubDeckResponse,
)
from app.utils.errors import DatabaseQueryFailed, TokenError
from app.validations.middleware_validation import validate_token
from services.subdeck_service import SubdeckService

subdeck_query = QueryType()


@subdeck_query.field("get_subdeck")
@validate_token
def resolve_get_subdeck(*_, subdeck_id: int, token: dict) -> SubDeckResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        user_info = token["user_info"]

        subdeck_service = SubdeckService(session=MySQLDB().session)
        subdeck = subdeck_service.validate_subdeck_user(user_id=user_info["id"], subdeck_id=subdeck_id)
        if not subdeck:
            return SubDeckResponse(
                response=Response(success=False, message="SubDeck não encontrado!")
            )

        subdeck = subdeck_service.get_subdeck(subdeck_id=subdeck_id)
        return SubDeckResponse(subdeck=subdeck, response=Response(success=True))

    except DatabaseQueryFailed:
        return SubDeckResponse(
            response=Response(success=False, message="Falha ao buscar SubDeck!")
        )

    except TokenError as error:
        return SubDeckResponse(response=Response(success=False, message=str(error)))

    except Exception as error:
        raise error
