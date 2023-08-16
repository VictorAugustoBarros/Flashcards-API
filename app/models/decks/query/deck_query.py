"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.deck_controller import DeckController
from app.models.decks.deck import Deck
from app.models.responses.deck_response import DeckResponse, DeckListResponse
from app.models.responses.response import Response
from app.utils.errors import DatabaseQueryFailed

deck_query = QueryType()
db_conn = Dependencies.create_database()
deck_controller = DeckController(db_conn=db_conn)


@deck_query.field("get_deck")
def resolve_get_deck(*_, deck_id: int) -> DeckResponse:
    """Busca do Deck pelo ID

    Args:
        *_:
        deck_id: ID do Deck

    Returns:
        Deck
    """
    try:
        deck = deck_controller.get_deck(deck_id=deck_id)

        return DeckResponse(deck=deck, response=Response(success=True))

    except DatabaseQueryFailed:
        return DeckResponse(
            response=Response(success=False, error="Falha ao buscar Deck")
        )

    except Exception as error:
        raise error


@deck_query.field("get_decks")
def resolve_get_decks(*_) -> DeckListResponse:
    """Busca de todos os Decks cadastrados

    Args:
        *_:

    Returns:
        List[Deck]: Lista com os Decks cadastrados
    """
    try:
        decks = deck_controller.get_all_decks()
        return DeckListResponse(decks=decks, response=Response(success=True))

    except DatabaseQueryFailed:
        return DeckListResponse(
            response=Response(success=False, error="Falha ao buscar Decks")
        )

    except Exception as error:
        raise error
