"""Card Response Model."""
from dataclasses import dataclass, field

from app.models.card import Card
from app.graphql_config.models.response import Response


@dataclass
class CardResponse:
    """Modelo de resposta do Card."""

    card: Card = None
    response: Response = None


@dataclass
class CardListResponse:
    """Modelo de resposta do Card."""

    cards: [Card] = field(default_factory=list)
    response: Response = None
