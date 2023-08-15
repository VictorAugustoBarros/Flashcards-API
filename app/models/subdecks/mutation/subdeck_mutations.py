"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.deck_controller import DeckController
from app.controllers.subdeck_controller import SubDeckController
from app.models.responses.response import Response
from app.models.responses.subdeck_response import SubDeckResponse
from app.models.subdecks.subdeck import SubDeck

subdeck_mutation = MutationType()
subdeck_controller = SubDeckController()
deck_controller = DeckController()


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

    except Exception as error:
        # TODO -> Criar exception generica para Falha de inserção
        return SubDeckResponse(
            response=Response(
                success=False, message="Falha ao criar Subdeck!", error=str(error)
            )
        )
