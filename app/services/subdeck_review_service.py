from app.models import SubDeckReview
from app.entities import SubDeckReviewEntity
from app.repository.subdeck_review_repository import SubDeckReviewRepository
from app.services.base_service import BaseService


class SubdeckReviewService(BaseService):
    def __init__(self, session):
        self.subdeck_review_repository = SubDeckReviewRepository(session=session)

    def create_subdeck_review(self, subdeck_review: SubDeckReview) -> SubDeckReview:
        subdeck_review_inserted: SubDeckReviewEntity = self.subdeck_review_repository.add(
            entity=SubDeckReviewEntity(
                **{
                    key: value
                    for key, value in subdeck_review.__dict__.items()
                    if value
                }
            )
        )
        subdeck_review.id = subdeck_review_inserted.id
        subdeck_review.deck_review_id = subdeck_review_inserted.deck_review_id
        subdeck_review.subdeck_id = subdeck_review_inserted.subdeck_id
        return subdeck_review

    def delete_subdeck_review(self, subdeck_review_id: int):
        self.subdeck_review_repository.remove(
            entity=SubDeckReviewEntity, document_id=subdeck_review_id
        )
        return True

    def get_subdeck_review(self, subdeck_review_id: int) -> SubDeckReview:
        subdeck_review: SubDeckReviewEntity = self.subdeck_review_repository.get_by_id(
            entity=SubDeckReviewEntity, document_id=subdeck_review_id
        )
        if not subdeck_review:
            return None

        return SubDeckReview(
            id=subdeck_review.id,
            deck_review_id=subdeck_review.deck_review_id,
            subdeck_id=subdeck_review.subdeck_id
        )

    def validate_subdeck_review_user(
        self, user_id: int, subdeck_review_id: int
    ) -> bool:
        return self.subdeck_review_repository.validate_subdeck_review(
            user_id=user_id, subdeck_review_id=subdeck_review_id
        )
