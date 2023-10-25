from dataclasses import dataclass


@dataclass
class CardReview:
    id: int = None
    card_id: int = None
    subdeck_review_id: int = None
    review_difficulties_id: int = None
    revision_date: str = None
