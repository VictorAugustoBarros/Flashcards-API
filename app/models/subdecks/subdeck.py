from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.models.cards.card import Card


@dataclass
class SubDeck:
    """Classe modelo do SubDeck."""

    name: str
    description: str
    cards: List[Card] = field(default_factory=list)
    creation_date: datetime = None
    id: int = None
