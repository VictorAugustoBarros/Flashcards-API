from sqlalchemy import and_

from app.entities import SubDeckReviewEntity, DeckEntity
from app.repository.base_repository import BaseRepository


class SubDeckReviewRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def validate_subdeck_review(self, user_id: int, subdeck_review_id: int) -> bool:
        deck = (
            self.session.query(SubDeckReviewEntity)
            .join(DeckEntity)
            .filter(
                and_(
                    DeckEntity.user_id == user_id,
                    SubDeckReviewEntity.id == subdeck_review_id,
                )
            )
            .first()
        )
        if not deck:
            return False

        return True
