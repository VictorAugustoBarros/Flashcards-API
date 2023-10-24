import datetime
from dataclasses import dataclass


@dataclass
class SubDeckReview:
    deck_id: int
    subdeck_id: int
    id: int = None
    creation_date: datetime = None
