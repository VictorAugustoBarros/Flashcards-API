"""Card Query GraphQL."""
from typing import List

from ariadne import QueryType

from app.graphql_config.models.card_response import CardListResponse
from app.graphql_config.models.response import Response
from app.graphql_config.models.subdeck_response import (
    SubDeckListResponse,
    SubDeckResponse,
)
from app.utils.errors import DatabaseQueryFailed, TokenError
from app.validations.middleware_validation import validate_token

subdeck_query = QueryType()


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


@subdeck_query.field("get_subdeck_cards")
@validate_token
def resolve_get_subdeck_cards(*_, subdeck_id: int, token: dict) -> CardListResponse:
    """Busca de todos os SubDecks cadastrados.

    Args:
        *_:
        subdeck_id(int): ID do SubDeck
        token(dict): Validação do Token

    Returns:
        CardListResponse: Lista com os Cards encontrados
    """
    try:
        if not token["valid"]:
            raise TokenError(token["error"])

        cards = card_controller.get_subdeck_cards(subdeck_id=subdeck_id)
        return CardListResponse(cards=cards, response=Response(success=True))

    except DatabaseQueryFailed:
        return CardListResponse(
            response=Response(success=False, error="Falha ao buscar Cards")
        )

    except TokenError as error:
        return CardListResponse(response=Response(success=False, error=str(error)))

    except Exception as error:
        raise error
