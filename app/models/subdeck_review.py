import datetime
from dataclasses import dataclass


@dataclass
class SubDeckReview:
    id: int = None
    deck_review_id: int = None
    subdeck_id: int = None
