import datetime
from dataclasses import dataclass


@dataclass
class UserDeck:
    """Classe modelo do Users."""

    user_id: int
    deck_id: int
    creation_date: datetime = None
