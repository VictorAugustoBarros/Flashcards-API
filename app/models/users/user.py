import datetime
from dataclasses import dataclass


@dataclass
class User:
    """Classe modelo do Users."""

    username: str
    email: str
    password: str
    creation_date: datetime = None
    id: int = None
