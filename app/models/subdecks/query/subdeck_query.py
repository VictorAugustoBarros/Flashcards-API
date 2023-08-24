"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.connections.dependencies import Dependencies
from app.controllers.subdeck_controller import SubDeckController
from app.models.responses.response import Response
from app.models.responses.subdeck_response import (SubDeckListResponse,
                                                   SubDeckResponse)
from app.models.subdecks.subdeck import SubDeck
from app.utils.errors import DatabaseQueryFailed

subdeck_query = QueryType()
db_conn = Dependencies.create_database()
subdeck_controller = SubDeckController(db_conn=db_conn)


@subdeck_query.field("get_subdeck")
def resolve_get_subdeck(*_, subdeck_id: int) -> SubDeckResponse:
    """Busca de um SubDeck

    Args:
        *_:
        subdeck_id(int): ID do subdeck

    Returns:
        SubDeck
    """
    try:
        subdeck = subdeck_controller.get_subdeck(subdeck_id=subdeck_id)
        return SubDeckResponse(subdeck=subdeck, response=Response(success=True))

    except DatabaseQueryFailed:
        return SubDeckResponse(
            response=Response(success=False, error="Falha ao buscar SubDeck")
        )

    except Exception as error:
        raise error


@subdeck_query.field("get_subdecks")
def resolve_get_subdecks(*_) -> SubDeckListResponse:
    """Busca de todos os SubDecks cadastrados.

    Args:
        *_:

    Returns:
        List[SubDeck]: Lista com os SubDecks
    """
    try:
        subdecks = subdeck_controller.get_all_subdecks()
        return SubDeckListResponse(subdecks=subdecks, response=Response(success=True))

    except DatabaseQueryFailed:
        return SubDeckListResponse(
            response=Response(success=False, error="Falha ao buscar SubDecks")
        )

    except Exception as error:
        raise error
