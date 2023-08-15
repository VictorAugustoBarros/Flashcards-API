"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.deck_controller import DeckController
from app.models.decks.deck import Deck
from app.models.responses.deck_response import DeckResponse
from app.models.responses.response import Response

deck_mutation = MutationType()
deck_controller = DeckController()


@deck_mutation.field("add_deck")
def resolve_add_deck(_, info, name: str, description: str) -> DeckResponse:
    """Inserção de um novo Deck

    Args:
        _:
        info:
        name: Nome do Deck
        description: Descrição do Deck

    Returns:
        DeckResponse
    """
    try:
        inserted_deck = deck_controller.insert_deck(
            deck=Deck(name=name, description=description)
        )

        return DeckResponse(
            deck=inserted_deck,
            response=Response(success=True, message="Deck criado com sucesso!"),
        )

    except Exception as error:
        DeckResponse(
            response=Response(
                success=False, message="Falha ao criar Deck!", error=str(error)
            )
        )
