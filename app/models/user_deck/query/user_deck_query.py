"""Card Query GraphQL."""
from ariadne import QueryType

from app.controllers.user_deck_controller import UserDeckController

user_deck_query = QueryType()
user_deck_controller = UserDeckController()


@user_deck_query.field("get_user_deck")
def resolve_get_user_deck(*_, user_id: int):
    decks = user_deck_controller.get_user_deck(user_id=user_id)

    return decks
