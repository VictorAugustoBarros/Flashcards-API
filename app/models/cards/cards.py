from dataclasses import dataclass
from datetime import datetime


@dataclass
class Card:
    question: str
    answer: str
    creation_date: datetime = None
