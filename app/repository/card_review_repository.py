from sqlalchemy import and_

from app.entities import CardReviewEntity, SubDeckReviewEntity, DeckReviewEntity, DeckEntity
from app.repository.base_repository import BaseRepository


class CardReviewRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def validate_card_review(self, user_id: int, card_review_id: int) -> bool:
        card = (
            self.session.query(CardReviewEntity)
            .join(SubDeckReviewEntity)
            .join(DeckReviewEntity)
            .join(DeckEntity)
            .filter(
                and_(
                    DeckEntity.user_id == user_id,
                    CardReviewEntity.id == card_review_id,
                )
            )
            .first()
        )
        if not card:
            return False

        return True
