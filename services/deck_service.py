from app.models.deck import Deck
from repository.deck_repository import DeckRepository
from entities.deck_entity import DeckEntity


class DeckService:
    def __init__(self, session):
        self.deck_repository = DeckRepository(session=session)

    def create_deck(self, deck: Deck):
        self.deck_repository.add(entity=DeckEntity)

    def delete_deck(self, deck_id: int):
        self.deck_repository.remove(entity=DeckEntity, document_id=deck_id)

    def update_deck(self, deck_id: int, deck: Deck):
        self.deck_repository.update(
            entity=DeckEntity, document_id=deck_id, document=deck.__dict__
        )

    def get_deck(self, deck_id: int):
        deck = self.deck_repository.get_by_id(entity=DeckEntity, document_id=deck_id)
        if not deck:
            return None

        return Deck(
            id=deck.id,
            name=deck.name,
            description=deck.description,
            creation_date=deck.creation_date,
        )
