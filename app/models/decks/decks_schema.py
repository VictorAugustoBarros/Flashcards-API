"""Deck."""
from typing import List

import strawberry

from app.models.cards import Card


@strawberry.type
class SubDeck:
    name: str
    description: str
    cards = List[Card]


# pylint: disable=R0903
@strawberry.type
class Deck:  # type: ignore
    """Classe modelo do Deck."""

    name: str
    description: str
    sub_deck: List[SubDeck]
