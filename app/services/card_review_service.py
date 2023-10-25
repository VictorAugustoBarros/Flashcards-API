from typing import Optional

from app.entities import CardReviewEntity
from app.repository.card_review_repository import CardReviewRepository
from app.services.base_service import BaseService
from app.models.card_review import CardReview


class CardReviewService(BaseService):
    def __init__(self, session):
        self.card_review_repository = CardReviewRepository(session=session)

    def create_card_review(self, card_review: CardReview):
        card_review_inserted: CardReviewEntity = self.card_review_repository.add(
            entity=CardReviewEntity(
                **{
                    key: value
                    for key, value in card_review.__dict__.items()
                    if value
                }
            )
        )
        card_review.id = card_review_inserted.id
        return card_review

    def delete_card_review(self, card_review_id: int):
        self.card_review_repository.remove(
            entity=CardReviewEntity, document_id=card_review_id
        )
        return True

    def get_card_review(self, card_review_id: int) -> Optional[CardReview]:
        card_review: CardReviewEntity = self.card_review_repository.get_by_id(
            entity=CardReviewEntity, document_id=card_review_id
        )
        if not card_review:
            return None

        return CardReview(
            id=card_review.id,
            card_id=card_review.card_id,
            review_difficulties_id=card_review.review_difficulties_id,
            subdeck_review_id=card_review.subdeck_review_id,
            revision_date=card_review.revision_date
        )

    def validate_card_review_user(self, user_id: int, card_review_id: int) -> bool:
        return self.card_review_repository.validate_card_review(
            user_id=user_id, card_review_id=card_review_id
        )
