from sqlalchemy import and_

from app.entities import DeckReviewEntity, DeckEntity
from app.repository.base_repository import BaseRepository


class DeckReviewRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def validate_deck_review(self, user_id: int, deck_review_id: int) -> bool:
        deck_review = (
            self.session.query(DeckReviewEntity)
            .join(DeckEntity)
            .filter(
                and_(
                    DeckEntity.user_id == user_id,
                    DeckReviewEntity.id == deck_review_id,
                )
            )
            .first()
        )
        if not deck_review:
            return False

        return True
