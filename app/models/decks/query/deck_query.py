"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.deck_controller import DeckController
from app.models.decks.deck import Deck
from app.models.responses.deck_response import DeckListResponse, DeckResponse
from app.models.responses.response import Response
from app.utils.errors import DatabaseQueryFailed, TokenError
from app.validations.middleware_validation import validate_token

deck_query = QueryType()
db_conn = Dependencies.create_database()
deck_controller = DeckController(db_conn=db_conn)


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

        deck = deck_controller.get_deck(deck_id=deck_id)

        return DeckResponse(deck=deck, response=Response(success=True))

    except DatabaseQueryFailed:
        return DeckResponse(
            response=Response(success=False, error="Falha ao buscar Deck")
        )

    except TokenError as error:
        return DeckResponse(response=Response(success=False, error=str(error)))

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
