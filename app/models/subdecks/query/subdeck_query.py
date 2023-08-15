"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.controllers.subdeck_controller import SubDeckController
from app.models.subdecks.subdeck import SubDeck

subdeck_query = QueryType()
subdeck_controller = SubDeckController()


@subdeck_query.field("get_subdeck")
def resolve_get_subdeck(*_, subdeck_id: int) -> SubDeck:
    """Busca de um SubDeck

    Args:
        *_:
        subdeck_id(int): ID do subdeck

    Returns:
        SubDeck
    """
    return subdeck_controller.get_subdeck(subdeck_id=subdeck_id)


@subdeck_query.field("get_subdecks")
def resolve_get_subdecks(*_) -> List[SubDeck]:
    """Busca de todos os SubDecks cadastrados.

    Args:
        *_:

    Returns:
        List[SubDeck]: Lista com os SubDecks
    """
    return subdeck_controller.get_all_subdecks()
