"""Deck Response Model"""
from dataclasses import dataclass

from app.models.responses.response import Response
from app.models.decks.deck import Deck


@dataclass
class DeckResponse:
    """Modelo de resposta do Deck."""

    deck: Deck = None
    response: Response = None
