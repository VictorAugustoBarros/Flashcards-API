from app.entities import DeckReviewEntity
from app.repository.deck_review_repository import DeckReviewRepository
from app.services.base_service import BaseService
from app.models.deck_review import DeckReview


class DeckReviewService(BaseService):
    def __init__(self, session):
        self.deck_review_repository = DeckReviewRepository(session=session)

    def create_deck_review(self, deck_review: DeckReview):
        deck_review_inserted: DeckReviewEntity = self.deck_review_repository.add(
            entity=DeckReviewEntity(
                **{
                    key: value
                    for key, value in deck_review.__dict__.items()
                    if value
                }
            )
        )
        deck_review.id = deck_review_inserted.id
        deck_review.creation_date = deck_review_inserted.revision_date
        return deck_review

    def delete_deck_review(self, deck_review_id: int):
        self.deck_review_repository.remove(
            entity=DeckReviewEntity, document_id=deck_review_id
        )
        return True

    def get_deck_review(self, deck_review_id: int) -> DeckReview:
        deck_review = self.deck_review_repository.get_by_id(
            entity=DeckReviewEntity, document_id=deck_review_id
        )
        if not deck_review:
            return None

        # TODO -> Retornar o model
        return DeckReview(
            id=deck_review.id,
            deck_id=deck_review.deck_id,
        )

    def validate_deck_review_user(self, user_id: int, deck_review_id: int) -> bool:
        return self.deck_review_repository.validate_deck_review(
            user_id=user_id, deck_review_id=deck_review_id
        )
