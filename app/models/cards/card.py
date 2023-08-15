"""Card Model."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Card:
    """Classe modelo do Card."""
    question: str
    answer: str
    creation_date: datetime = None
    id: int = None
