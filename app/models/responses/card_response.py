"""Card Response Model."""
from dataclasses import dataclass

from app.models.responses.response import Response
from app.models.cards.card import Card


@dataclass
class CardResponse:
    """Modelo de resposta do Card."""

    card: Card = None
    response: Response = None
