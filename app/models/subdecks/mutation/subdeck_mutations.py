"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.connections.dependencies import Dependencies
from app.controllers.deck_controller import DeckController
from app.controllers.subdeck_controller import SubDeckController
from app.models.responses.response import Response
from app.models.responses.subdeck_response import SubDeckResponse
from app.models.subdecks.subdeck import SubDeck
from app.utils.errors import DatabaseInsertFailed, DatabaseQueryFailed

subdeck_mutation = MutationType()
db_conn = Dependencies.create_database()
subdeck_controller = SubDeckController(db_conn=db_conn)
deck_controller = DeckController(db_conn=db_conn)


@subdeck_mutation.field("add_subdeck")
def resolve_add_subdeck(
    _, info, deck_id: int, name: str, description: str
) -> SubDeckResponse:
    """Inserção de um novo SubDeck

    Args:
        _:
        info:
        deck_id(int): ID do Deck
        name(str): Nome do Deck
        description(str): Descrição do Deck

    Returns:
        SubDeckResponse
    """
    try:
        deck_exists = deck_controller.validate_deck_exists(deck_id=deck_id)
        if not deck_exists:
            return SubDeckResponse(
                response=Response(
                    success=False, message="Não existe um Deck com esse ID!"
                )
            )

        sub_deck = SubDeck(name=name, description=description)
        inserted_subdeck = subdeck_controller.insert_subdeck(
            subdeck=sub_deck, deck_id=deck_id
        )

        return SubDeckResponse(
            subdeck=inserted_subdeck,
            response=Response(success=True, message="Subdeck criado com sucesso!"),
        )

    except (DatabaseInsertFailed, DatabaseQueryFailed):
        return SubDeckResponse(
            response=Response(success=False, error="Falha ao criar Subdeck!")
        )

    except Exception as error:
        raise error
