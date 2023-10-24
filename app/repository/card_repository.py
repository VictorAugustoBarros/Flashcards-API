"""Card Repository."""
from datetime import datetime

from sqlalchemy import and_

from app.entities import CardEntity, SubDeckEntity, DeckEntity
from app.repository.base_repository import BaseRepository


class CardRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def validate_card(self, user_id: int, card_id: int) -> bool:
        card = (
            self.session.query(CardEntity)
            .join(SubDeckEntity)
            .join(DeckEntity)
            .filter(and_(DeckEntity.user_id == user_id, CardEntity.id == card_id))
            .first()
        )
        if not card:
            return False

        return True

    def create_card_review(self, card_id: int, review_difficulties_id: int) -> bool:
        card = self.session.query(CardEntity).filter(CardEntity.id == card_id).first()
        card.revised = True
        card.review_difficulties_id = review_difficulties_id
        card.revision_date = datetime.now()
        self.session.commit()
        return True
