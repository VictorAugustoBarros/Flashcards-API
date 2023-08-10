"""Deck."""
from typing import List

import strawberry

from app.models.cards import Card


# pylint: disable=R0903
@strawberry.type
class Deck:  # type: ignore
    """Classe modelo do Deck."""

    name: str
    description: str
    cards = List[Card]
