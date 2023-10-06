"""Subdeck Model."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from app.models.card import Card


@dataclass
class SubDeck:
    """Classe modelo do SubDeck."""

    name: str
    description: str
    id: int = None
    creation_date: datetime = None
    deck_id: int = None
    cards: List[Card] = field(default_factory=list)
