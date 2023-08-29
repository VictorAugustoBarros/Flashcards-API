"""Card Query GraphQL."""
from typing import List, Optional, Union

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.user_subdeck_controller import UserSubDeckController
from app.models.responses.response import Response
from app.models.responses.subdeck_response import SubDeckListResponse
from app.models.subdecks.subdeck import SubDeck
from app.utils.errors import TokenError
from app.validations.middleware_validation import validate_token

user_subdeck_query = QueryType()
db_conn = Dependencies.create_database()
user_subdeck_controller = UserSubDeckController(db_conn=db_conn)


@user_subdeck_query.field("get_user_subdeck")
@validate_token
def resolve_get_user_subdeck(*_, token: dict) -> SubDeckListResponse:
    """Busca dos Subdecks do usuário

    Args:
        *_:
        token(dict): Token do usuário

    Returns:

    """
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        subdecks = user_subdeck_controller.get_user_subdeck(user_id=user_info["id"])
        return SubDeckListResponse(subdecks=subdecks, response=Response(success=True))

    except TokenError as error:
        return SubDeckListResponse(response=Response(success=False, error=str(error)))

    except Exception as error:
        return SubDeckListResponse(response=Response(success=False, error="Falha ao criar Card!"))
