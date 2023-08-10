"""Card Mutations GraphQL."""
import strawberry

from app.controllers.card_controller import CardController
from app.models.cards import Card


# pylint: disable=R0903
@strawberry.type
class Mutation:
    """Classe Mutations GraphQL."""

    @strawberry.mutation
    def add_card(self, question: str, answer: str) -> Card:
        """Inserção de um novo Card

        Args:
            question (str): Pergunta do Card
            answer (str): Resposta do Card

        Returns:
            card (Card): Card inserido
        """
        card = Card(question=question, answer=answer)
        if question and answer:
            card_controller = CardController()
            card_controller.insert_card(card=card)

        return card
