"""Card Query GraphQL."""
import sentry_sdk
from ariadne import QueryType

from app.connections.mysql import MySQLDB
from app.graphql_config.models.card_response import CardListResponse, CardResponse
from app.graphql_config.models.response import Response
from app.utils.errors import DatabaseQueryFailed, TokenError
from app.validations.middleware_validation import validate_token
from services.card_service import CardService

card_query = QueryType()


@card_query.field("get_card")
@validate_token
def resolve_get_card(*_, card_id: int, token: dict) -> CardResponse:
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        card_service = CardService(session=MySQLDB().session)

        card_user = card_service.validate_card_user(
            user_id=user_info["id"], card_id=card_id
        )
        if not card_user:
            return CardResponse(
                response=Response(success=False, message="Card não encontrado!")
            )

        card = card_service.get_card(card_id=card_id)

        return CardResponse(card=card, response=Response(success=True))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return CardResponse(
            response=Response(success=False, message="Falha ao buscar Card")
        )
