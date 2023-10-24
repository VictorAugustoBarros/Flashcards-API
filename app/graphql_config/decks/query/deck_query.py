"""Card Query GraphQL."""
import sentry_sdk
from ariadne import QueryType

from app.connections.mysql import MySQLDB
from app.graphql_config.models.deck_response import DeckResponse
from app.graphql_config.models.response import Response
from app.utils.errors import DatabaseQueryFailed, TokenError
from app.utils.middleware_validation import validate_token
from app.services.deck_service import DeckService

deck_query = QueryType()


@deck_query.field("get_deck")
@validate_token
def resolve_get_deck(*_, deck_id: int, token: dict) -> DeckResponse:
    """Busca do Deck pelo ID

    Args:
        *_:
        deck_id(int): ID do Deck
        token(dict): Validação do Token

    Returns:
        Deck
    """
    try:
        if not token["valid"]:
            raise TokenError(token["error"])
        user_info = token["user_info"]

        deck_service = DeckService(session=MySQLDB().session)
        deck_user = deck_service.validate_deck_user(
            user_id=user_info["id"], deck_id=deck_id
        )
        if not deck_user:
            return DeckResponse(
                response=Response(success=False, message="Deck não encontrado!")
            )

        deck = deck_service.get_deck(deck_id=deck_id)
        return DeckResponse(deck=deck, response=Response(success=True))

    except DatabaseQueryFailed:
        return DeckResponse(
            response=Response(success=False, message="Falha ao buscar Deck")
        )

    except TokenError as error:
        return DeckResponse(response=Response(success=False, message=str(error)))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return DeckResponse(
            response=Response(success=False, message="Falha ao remover Review!")
        )
