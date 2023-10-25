from dataclasses import dataclass


@dataclass
class DeckReview:
    deck_id: int
    id: int = None
    revised: str = None
    revision_date: str = None
