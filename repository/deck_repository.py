"""Deck Repository."""
from repository.base_repository import BaseRepository


class DeckRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()
