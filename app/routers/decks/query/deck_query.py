"""Deck Query GraphQL."""
import typing

import strawberry

from app.models.deck import Deck


# pylint: disable=R0903
@strawberry.type
class DeckQuery:
    """Classe Query GraphQL."""

    decks: typing.List[Deck] = strawberry.field()
