"""Card Model."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Card:
    """Classe modelo do Card."""

    question: str
    answer: str
    subdeck_id: int = None
    creation_date: datetime = None
    id: int = None  # pylint: disable=C0103
