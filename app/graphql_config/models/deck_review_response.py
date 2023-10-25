from dataclasses import dataclass

from app.graphql_config.models.response import Response
from app.models.deck_review import DeckReview


@dataclass
class DeckReviewResponse:
    """Modelo de resposta do DeckReviewResponse."""

    deck_review: DeckReview = None
    response: Response = None
