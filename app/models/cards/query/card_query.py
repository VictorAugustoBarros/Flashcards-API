"""Card Query GraphQL."""
from graphene import List, ObjectType, Field, String
from graphene.types.generic import GenericScalar

from app.models.cards.schema.cards_schema import Card
from app.controllers.card_controller import CardController


class CardQuery(ObjectType):
    """Classe Query GraphQL."""
    cards = List(Card)

    get_question = Field(Card, question=String())

    def resolve_cards(root, info):
        card_controller = CardController()
        cards = card_controller.get_all_cards()
        return cards

    def resolve_get_question(root, info, question: str):
        card_controller = CardController()
        return card_controller.get_question(question=question)
