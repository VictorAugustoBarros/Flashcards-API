"""SubDeck Repository."""
from sqlalchemy import and_

from app.entities import SubDeckEntity, DeckEntity
from app.repository.base_repository import BaseRepository


class SubDeckRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def validate_subdeck(self, user_id: int, subdeck_id: int) -> bool:
        subdeck = (
            self.session.query(SubDeckEntity)
            .join(DeckEntity)
            .filter(and_(DeckEntity.user_id == user_id, SubDeckEntity.id == subdeck_id))
            .first()
        )
        if not subdeck:
            return False

        return True
