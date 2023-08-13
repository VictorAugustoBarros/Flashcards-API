"""Card Query GraphQL."""
from ariadne import QueryType

from app.controllers.card_controller import CardController

card_query = QueryType()
card_controller = CardController()


@card_query.field("get_card")
def resolve_get_cards(*_, card_id: int):
    card = card_controller.get_card(card_id=card_id)
    return card


@card_query.field("get_cards")
def resolve_get_cards(*_):
    cards = card_controller.get_all_cards()

    return cards
