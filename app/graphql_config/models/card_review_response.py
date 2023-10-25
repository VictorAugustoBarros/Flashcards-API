from dataclasses import dataclass

from app.graphql_config.models.response import Response
from app.models.card_review import CardReview


@dataclass
class CardReviewResponse:
    """Modelo de resposta do DeckReviewResponse."""

    card_review: CardReview = None
    response: Response = None
