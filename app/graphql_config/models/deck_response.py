"""Deck Response Model"""
from dataclasses import dataclass

from app.models.deck import Deck
from app.graphql_config.models.response import Response


@dataclass
class DeckResponse:
    """Modelo de resposta do Deck."""

    deck: Deck = None
    response: Response = None


@dataclass
class DeckListResponse:
    """Modelo de resposta do Deck."""

    decks: [Deck] = None
    response: Response = None
