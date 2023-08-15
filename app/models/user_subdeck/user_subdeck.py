import datetime
from dataclasses import dataclass


@dataclass
class UserSubSeck:
    """Classe modelo do Users."""

    user_id: int
    subdeck_id: int
    creation_date: datetime = None
