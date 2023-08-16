"""Subdeck Response Model."""
from dataclasses import dataclass, field

from app.models.responses.response import Response
from app.models.subdecks.subdeck import SubDeck


@dataclass
class SubDeckResponse:
    """Modelo de resposta do SubDeck."""

    subdeck: SubDeck = None
    response: Response = None


@dataclass
class SubDeckListResponse:
    """Modelo de resposta do SubDeck."""

    subdecks: [SubDeck] = field(default_factory=list)
    response: Response = None
