"""Card Repository."""
from sqlalchemy import and_

from entities import CardEntity, SubDeckEntity, DeckEntity
from repository.base_repository import BaseRepository


class CardRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def get_cards_user(self):
        ...

    def validate_card(self, user_id: int, card_id: int) -> bool:
        card = (
            self.session.query(CardEntity)
            .join(SubDeckEntity)
            .join(DeckEntity)
            .filter(and_(DeckEntity.user_id == user_id, CardEntity.id == card_id))
            .first()
        )
        if not card:
            return False

        return True
