"""Card Query GraphQL."""
import typing
from typing import Optional, Union

import strawberry

from app.controllers.card_controller import CardController
from app.models.cards import Card


# pylint: disable=R0903
@strawberry.type
class CardQuery:
    """Classe Query GraphQL."""

    cards: typing.List[Card] = strawberry.field(resolver=CardController().get_all_cards)

    @strawberry.field()
    def get_question(self, question: str) -> Optional[Union[Card, None]]:
        """Busca de um Card pela variavel *question*

        Args:
            question (str): Question a ser pesquisada

        Returns:
        """
        return CardController().get_question(question=question)
