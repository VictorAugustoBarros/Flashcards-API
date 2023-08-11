"""Card Mutations GraphQL."""
from graphene import Mutation, String, Boolean, Field, ObjectType
from app.controllers.card_controller import CardController
from app.errors import CreateCardError
from app.models.cards.schema.cards_schema import Card


class CreateCard(Mutation):
    class Arguments:
        question = String(required=True)
        answer = String(required=True)

    created = Boolean()
    message = String()
    card = Field(Card)

    def mutate(self, info, question: str, answer: str):
        card = Card(question=question, answer=answer)

        try:
            card_controller = CardController()
            card_controller.insert_card(card)

        except CreateCardError:
            return CreateCard(created=False, message="Falha ao inserir Card!")

        return CreateCard(card=card, created=True, message="Card inserido com sucesso!")


class CardMutation(ObjectType):
    create_card = CreateCard.Field()
