"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.deck_controller import DeckController
from app.models.decks.decks import Deck

deck_mutation = MutationType()
deck_controller = DeckController()


@deck_mutation.field("add_deck")
def resolve_add_deck(_, info, name: str, description: str):
    try:
        deck_controller.insert_deck(deck=Deck(name=name, description=description))
        return {"success": True, "message": "Deck criado com sucesso!"}

    except Exception as error:
        return {
            "success": False,
            "message": "Falha ao criar Deck!",
            "error": str(error),
        }
