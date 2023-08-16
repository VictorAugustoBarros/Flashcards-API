"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.user_deck_controller import UserDeckController
from app.models.decks.deck import Deck
from app.models.responses.deck_response import DeckListResponse
from app.models.responses.response import Response
from app.utils.errors import DatabaseQueryFailed

user_deck_query = QueryType()
db_conn = Dependencies.create_database()
user_deck_controller = UserDeckController(db_conn=db_conn)


@user_deck_query.field("get_user_deck")
def resolve_get_user_deck(*_, user_id: int) -> DeckListResponse:
    """Busca dos decks cadastrados do usuário

    Args:
        *_:
        user_id: ID do usuário

    Returns:
        List[Deck]: Lista com os Decks cadastrados
    """
    try:
        user_decks = user_deck_controller.get_user_deck(user_id=user_id)

        return DeckListResponse(decks=user_decks, response=Response(success=True))

    except DatabaseQueryFailed:
        return DeckListResponse(
            response=Response(success=False, error="Falha ao buscar Decks")
        )

    except Exception as error:
        raise error
