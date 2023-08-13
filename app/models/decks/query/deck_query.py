"""Card Query GraphQL."""
from ariadne import QueryType

from app.controllers.deck_controller import DeckController

deck_query = QueryType()
deck_controller = DeckController()


@deck_query.field("get_decks")
def resolve_get_decks(*_):
    decks = deck_controller.get_all_decks()

    return decks


@deck_query.field("get_deck")
def resolve_get_decks(*_, deck_id: int):
    deck = deck_controller.get_deck(deck_id=deck_id)

    return deck
