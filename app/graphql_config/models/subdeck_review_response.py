from dataclasses import dataclass

from app.graphql_config.models.response import Response
from app.models.subdeck_review import SubDeckReview


@dataclass
class SubDeckReviewResponse:
    """Modelo de resposta do SubDeckReviewResponse."""

    subdeck_review: SubDeckReview = None
    response: Response = None
