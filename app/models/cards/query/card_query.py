"""Card Query GraphQL."""
from typing import List, Optional

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.card_controller import CardController
from app.models.cards.card import Card
from app.models.responses.card_response import CardListResponse, CardResponse
from app.models.responses.response import Response
from app.utils.errors import DatabaseQueryFailed

card_query = QueryType()
db_conn = Dependencies.create_database()
card_controller = CardController(db_conn=db_conn)


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
        card = card_controller.get_card(card_id=card_id)
        return CardResponse(card=card, response=Response(success=True))

    except DatabaseQueryFailed:
        return CardResponse(
            response=Response(success=False, error="Falha ao buscar Card")
        )

    except Exception as error:
        raise error


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
