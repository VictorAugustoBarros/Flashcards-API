from typing import Optional

from app.utils.jwt_manager import JwtManager
from app.models.deck import Deck
from app.utils.errors import UsernameAlreadyTaken, EmailAlreadyTaken
from app.entities.user_entity import UserEntity
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, session):
        self.user_repository = UserRepository(session=session)

    def get_user_flashcards(self, user_id: int):
        decks = self.user_repository.get_by_id(entity=UserEntity, document_id=user_id)
        if not decks:
            return None

        user_decks = []
        for deck in decks.deck:
            deck_subdecks = []
            if subdecks := deck.subdeck:
                deck_subdecks = self.get_subdecks(subdecks=subdecks)

            user_decks.append(
                Deck(
                    id=deck.id,
                    name=deck.name,
                    description=deck.description,
                    creation_date=deck.creation_date,
                    user_id=deck.user_id,
                    subdecks=deck_subdecks,
                )
            )

        return user_decks

    def get_user(self, user_id: int) -> Optional[User]:
        user = self.user_repository.get_by_id(entity=UserEntity, document_id=user_id)
        if not user:
            return None

        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            creation_date=user.creation_date,
        )

    def create_user(self, user: User) -> bool:
        username_exists = self.user_repository.validate_username(username=user.username)
        if username_exists:
            raise UsernameAlreadyTaken()

        email_exists = self.user_repository.validate_email(email=user.email)
        if email_exists:
            raise EmailAlreadyTaken()

        user_entity = UserEntity(**user.__dict__)
        self.user_repository.add(entity=user_entity)

        return True

    def update_user(self, user: User):
        self.user_repository.update(
            entity=UserEntity,
            document_id=user.id,
            document={
                "username": user.username,
                "email": user.email,
                "password": user.password,
            },
        )
        return True

    # TODO -> Validar a remoção dos registros FK antes de deletar o User
    def delete_user(self, user_id: int) -> bool:
        self.user_repository.remove(entity=UserEntity, document_id=user_id)
        return True

    def validate_username(self, username: str) -> bool:
        return self.user_repository.validate_username(username=username)

    def login(self, email: str, password: str):
        user = self.user_repository.login(email=email, password=password)
        if not user:
            return None

        jwt_token = JwtManager.create_token(
            user_data={
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }
        )
        return jwt_token
