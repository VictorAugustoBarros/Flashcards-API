"""Card Mutations GraphQL."""
from ariadne import MutationType

from app.controllers.card_controller import CardController

from app.models.cards.cards import Card

card_mutation = MutationType()
card_controller = CardController()


@card_mutation.field("add_card")
def resolve_add_card(_, info, question: str, answer: str):
    try:
        card_controller.insert_card(card=Card(question=question, answer=answer))
        return {"success": True, "message": "Card criado com sucesso!"}

    except Exception as error:
        return {
            "success": False,
            "message": "Falha ao criar Card!",
            "error": str(error),
        }
