"""Deck Model."""
import datetime
from dataclasses import dataclass, field
from typing import List

from app.models.subdeck import SubDeck


@dataclass
class Deck:
    """Classe modelo do Deck."""

    name: str
    description: str
    creation_date: datetime = None
    user_id: int = None
    id: int = None
    subdecks: List[SubDeck] = field(default_factory=list)
