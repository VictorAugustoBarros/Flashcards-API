"""Deck Repository."""
from sqlalchemy import and_

from app.entities import DeckEntity
from app.repository.base_repository import BaseRepository


class DeckRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def validate_deck(self, user_id: int, deck_id: int) -> bool:
        deck = (
            self.session.query(DeckEntity)
            .filter(and_(DeckEntity.user_id == user_id, DeckEntity.id == deck_id))
            .first()
        )
        if not deck:
            return False

        return True
