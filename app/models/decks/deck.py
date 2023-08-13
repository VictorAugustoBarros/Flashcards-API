import datetime
from dataclasses import dataclass
from typing import List

from app.models.subdecks.subdeck import SubDeck


@dataclass
class Deck:
    """Classe modelo do Deck."""

    name: str
    description: str
    sub_deck: List[SubDeck]
    creation_date: datetime = None
    id: int = None
