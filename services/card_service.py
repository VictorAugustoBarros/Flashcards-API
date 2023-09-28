from app.models.card import Card
from repository.card_repository import CardRepository
from entities.card_entity import CardEntity


class CardService:
    def __init__(self, session):
        self.card_repository = CardRepository(session=session)

    def create_card(self, card: Card):
        self.card_repository.add(entity=CardEntity)

    def delete_card(self, card_id: int):
        self.card_repository.remove(entity=CardEntity, document_id=card_id)

    def update_card(self, card_id: int, card: Card):
        self.card_repository.update(entity=CardEntity, document_id=card_id, document=card.__dict__)

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
