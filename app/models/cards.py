"""Cards."""
from datetime import datetime
from typing import List

import strawberry


# pylint: disable=R0903
@strawberry.type
class AdditionalInfo:
    """Classe modelo para os dados adicionais."""

    text: str = ""
    image: str = ""


# pylint: disable=R0903
@strawberry.type
class Card:
    """Classe modelo Card."""

    question: str
    answer: str
    insert_date: datetime = datetime.now()
    additional_info: List[AdditionalInfo] = strawberry.field(default_factory=list)
