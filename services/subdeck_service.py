from app.models.subdeck import SubDeck
from repository.subdeck_repository import SubDeckRepository
from entities.subdeck_entity import SubDeckEntity
from services.base_service import BaseService


class SubdeckService(BaseService):
    def __init__(self, session):
        self.subdeck_repository = SubDeckRepository(session=session)

    def create_subdeck(self, subdeck: SubDeck):
        subdeck_inserted = self.subdeck_repository.add(
            entity=SubDeckEntity(**subdeck.__dict__)
        )
        subdeck.id = subdeck_inserted.id
        subdeck.creation_date = subdeck_inserted.creation_date
        return subdeck

    def delete_subdeck(self, subdeck_id: int):
        self.subdeck_repository.remove(entity=SubDeckEntity, document_id=subdeck_id)
        return True

    def update_subdeck(self, subdeck_id: int, subdeck: SubDeck):
        self.subdeck_repository.update(
            entity=SubDeckEntity,
            document_id=subdeck_id,
            document={
                key: value.strip() for key, value in subdeck.__dict__.items() if value
            },
        )
        return True

    def validate_subdeck_user(self, user_id: int, subdeck_id: int) -> bool:
        return self.subdeck_repository.validate_subdeck(
            user_id=user_id, subdeck_id=subdeck_id
        )

    def get_subdeck(self, subdeck_id: int):
        subdeck = self.subdeck_repository.get_by_id(
            entity=SubDeckEntity, document_id=subdeck_id
        )
        if not subdeck:
            return None

        subdeck_cards = []
        if cards := subdeck.cards:
            subdeck_cards = self.get_cards(cards=cards)

        return SubDeck(
            id=subdeck.id,
            name=subdeck.name,
            description=subdeck.description,
            creation_date=subdeck.creation_date,
            cards=subdeck_cards,
        )
