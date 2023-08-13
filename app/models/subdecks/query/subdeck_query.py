"""Card Query GraphQL."""
from ariadne import QueryType

from app.controllers.subdeck_controller import SubDeckController

subdeck_query = QueryType()
subdeck_controller = SubDeckController


@subdeck_query.field("get_subdecks")
def resolve_get_subdecks(*_):
    decks = subdeck_controller.get_all_subdecks()

    return decks
