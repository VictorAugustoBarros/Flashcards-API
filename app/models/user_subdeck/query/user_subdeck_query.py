"""Card Query GraphQL."""
from ariadne import QueryType

from app.controllers.user_subdeck_controller import UserSubDeckController

user_subdeck_query = QueryType()
user_subdeck_controller = UserSubDeckController()


@user_subdeck_query.field("get_user_subdeck")
def resolve_get_user_subdeck(*_, user_id: int):
    decks = user_subdeck_controller.get_user_subdeck(user_id=user_id)

    return decks
