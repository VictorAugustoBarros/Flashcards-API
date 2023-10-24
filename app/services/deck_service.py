from app.models.deck import Deck
from app.repository.deck_repository import DeckRepository
from app.entities.deck_entity import DeckEntity
from app.services.base_service import BaseService


class DeckService(BaseService):
    def __init__(self, session):
        self.deck_repository = DeckRepository(session=session)

    def create_deck(self, deck: Deck):
        deck_inserted = self.deck_repository.add(
            entity=DeckEntity(
                **{key: value for key, value in deck.__dict__.items() if value}
            )
        )
        deck.id = deck_inserted.id
        deck.creation_date = deck_inserted.creation_date
        return deck

    def delete_deck(self, deck_id: int):
        self.deck_repository.remove(entity=DeckEntity, document_id=deck_id)
        return True

    def update_deck(self, deck_id: int, deck: Deck) -> bool:
        self.deck_repository.update(
            entity=DeckEntity,
            document_id=deck_id,
            document={
                key: value.strip() for key, value in deck.__dict__.items() if value
            },
        )
        return True

    def validate_deck_user(self, user_id: int, deck_id: int) -> bool:
        return self.deck_repository.validate_deck(user_id=user_id, deck_id=deck_id)

    def get_deck(self, deck_id: int):
        deck = self.deck_repository.get_by_id(entity=DeckEntity, document_id=deck_id)
        if not deck:
            return None

        deck_subdecks = []
        if subdecks := deck.subdeck:
            deck_subdecks = self.get_subdecks(subdecks=subdecks)

        return Deck(
            id=deck.id,
            name=deck.name,
            description=deck.description,
            creation_date=deck.creation_date,
            user_id=deck.user_id,
            subdecks=deck_subdecks,
        )
