import datetime
from typing import List
from dataclasses import dataclass

from app.models.cards.cards import Card


@dataclass
class SubDeck:
    """Classe modelo do SubDeck."""

    name: str
    description: str
    cards = List[Card]


@dataclass
class Deck:
    """Classe modelo do Deck."""

    name: str
    description: str
    sub_deck: List[SubDeck]
    creation_date: datetime = None
