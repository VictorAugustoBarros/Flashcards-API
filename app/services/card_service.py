from app.models.card import Card
from app.repository.card_repository import CardRepository
from app.entities.card_entity import CardEntity


class CardService:
    def __init__(self, session):
        self.card_repository = CardRepository(session=session)

    def create_card(self, card: Card) -> Card:
        card_inserted = self.card_repository.add(
            entity=CardEntity(
                **{key: value for key, value in card.__dict__.items() if value}
            )
        )
        card.id = card_inserted.id
        card.creation_date = card_inserted.creation_date
        return card

    def delete_card(self, card_id: int):
        self.card_repository.remove(entity=CardEntity, document_id=card_id)
        return True

    def update_card(self, card_id: int, card: Card):
        self.card_repository.update(
            entity=CardEntity,
            document_id=card_id,
            document={key: value for key, value in card.__dict__.items() if value},
        )
        return True

    def validate_card_user(self, user_id: int, card_id: int) -> bool:
        return self.card_repository.validate_card(user_id=user_id, card_id=card_id)

    def get_card(self, card_id: int):
        card = self.card_repository.get_by_id(entity=CardEntity, document_id=card_id)
        if not card:
            return None

        return Card(
            id=card.id,
            question=card.question,
            answer=card.answer,
            creation_date=card.creation_date,
        )

    def create_card_review(self, card_id: int, review_difficulties_id: int):
        return self.card_repository.create_card_review(
            card_id=card_id, review_difficulties_id=review_difficulties_id
        )
