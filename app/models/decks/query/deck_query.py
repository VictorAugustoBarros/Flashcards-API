"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.controllers.deck_controller import DeckController
from app.models.decks.deck import Deck

deck_query = QueryType()
deck_controller = DeckController()


@deck_query.field("get_deck")
def resolve_get_deck(*_, deck_id: int) -> Deck:
    """Busca do Deck pelo ID

    Args:
        *_:
        deck_id: ID do Deck

    Returns:
        Deck
    """
    try:
        return deck_controller.get_deck(deck_id=deck_id)

    except Exception as error:
        raise error


@deck_query.field("get_decks")
def resolve_get_decks(*_) -> List[Deck]:
    """Busca de todos os Decks cadastrados

    Args:
        *_:

    Returns:
        List[Deck]: Lista com os Decks cadastrados
    """
    try:
        return deck_controller.get_all_decks()

    except Exception as error:
        raise error
