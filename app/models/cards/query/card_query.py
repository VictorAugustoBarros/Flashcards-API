"""Card Query GraphQL."""
from typing import Optional, List
from ariadne import QueryType

from app.controllers.card_controller import CardController
from app.models.cards.card import Card

card_query = QueryType()
card_controller = CardController()


@card_query.field("get_card")
def resolve_get_card(*_, card_id: int) -> Optional[Card]:
    """Busca do Card por ID

    Args:
        *_:
        card_id (int): ID do Card

    Returns:
        card(Card): Card encontrado
    """
    card = card_controller.get_card(card_id=card_id)
    return card


@card_query.field("get_cards")
def resolve_get_cards(*_) -> List[Card]:
    """Busca dos cards cadastrados

    Args:
        *_:

    Returns:
        cards(List[Card]): Lista de Cards
    """
    cards = card_controller.get_all_cards()

    return cards
