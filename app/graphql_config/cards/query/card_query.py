"""Card Query GraphQL."""
import sentry_sdk
from ariadne import QueryType

from app.connections.mysql import MySQLDB
from app.graphql_config.models.card_response import CardListResponse, CardResponse
from app.graphql_config.models.response import Response
from app.utils.errors import DatabaseQueryFailed
from services.card_service import CardService

card_query = QueryType()


@card_query.field("get_card")
def resolve_get_card(*_, card_id: int) -> CardResponse:
    """Busca do Card por ID

    Args:
        *_:
        card_id (int): ID do Card

    Returns:
        card(Card): Card encontrado
    """
    try:
        card_service = CardService(session=MySQLDB().session)
        card = card_service.get_card(card_id=card_id)
        if not card:
            return CardResponse(response=Response(success=False, message="Card não encontrado!"))

        return CardResponse(card=card, response=Response(success=True))

    except Exception as error:
        sentry_sdk.capture_exception(error)
        return CardResponse(
            response=Response(success=False, message="Falha ao buscar Card")
        )


@card_query.field("get_cards")
def resolve_get_cards(*_) -> CardListResponse:
    """Busca dos cards cadastrados

    Args:
        *_:

    Returns:
        cards(List[Card]): Lista de Cards
    """
    try:
        cards = card_controller.get_all_cards()
        return CardListResponse(cards=cards, response=Response(success=True))

    except DatabaseQueryFailed:
        return CardListResponse(
            response=Response(success=False, error="Falha ao buscar Cards")
        )

    except Exception as error:
        raise error
