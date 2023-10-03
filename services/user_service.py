from typing import Optional

from app.jwt_manager import JwtManager
from entities.user_entity import UserEntity
from app.models.user import User
from repository.user_repository import UserRepository


class UserService:
    def __init__(self, session):
        self.user_repository = UserRepository(session=session)

    def get_user(self, user_id: int) -> Optional[User]:
        user = self.user_repository.get_by_id(entity=UserEntity, document_id=user_id)
        if not user:
            return None

        return User(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
            creation_date=user.creation_date
        )

    def create_user(self, user: User) -> bool:
        username_exists = self.user_repository.validate_username(username=user.username)
        if username_exists:
            return False

        email_exists = self.user_repository.validate_email(email=user.email)
        if email_exists:
            return False

        user_entity = UserEntity(**user.__dict__)
        self.user_repository.add(entity=user_entity)

        return True

    def update_user(self, user: User):
        self.user_repository.update(entity=UserEntity, document_id=user.id, document={
            "username": user.username,
            "email": user.email,
            "password": user.password
        })
        return True

    def delete_user(self, user_id: int) -> bool:
        self.user_repository.remove(entity=UserEntity, document_id=user_id)
        return True

    def validate_username(self, username: str) -> bool:
        return self.user_repository.validate_username(username=username)

    def validate_user(self, user: User):
        user_exists = self.user_repository.validate_user(user_id=user.id)
        if not user_exists:
            return False

        return True

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
