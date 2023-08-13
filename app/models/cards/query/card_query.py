"""Card Query GraphQL."""
from ariadne import QueryType

from app.controllers.card_controller import CardController

card_query = QueryType()
card_controller = CardController()


@card_query.field("get_cards")
def resolve_get_cards(*_):
    cards = card_controller.get_all_cards()

    return cards
