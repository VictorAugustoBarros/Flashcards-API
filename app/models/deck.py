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
    sub_deck: List[SubDeck] = field(default_factory=list)
    creation_date: datetime = None
    id: int = None  # pylint: disable=C0103
