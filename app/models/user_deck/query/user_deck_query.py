"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.controllers.user_deck_controller import UserDeckController
from app.models.decks.deck import Deck

user_deck_query = QueryType()
user_deck_controller = UserDeckController()


@user_deck_query.field("get_user_deck")
def resolve_get_user_deck(*_, user_id: int) -> List[Deck]:
    """Busca dos decks cadastrados do usuário

    Args:
        *_:
        user_id: ID do usuário

    Returns:
        List[Deck]: Lista com os Decks cadastrados
    """
    return user_deck_controller.get_user_deck(user_id=user_id)
