"""Card Repository."""
from repository.base_repository import BaseRepository

from entities.user_entity import UserEntity


class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.session = session()

    def delete_user(self, user_id: int):
        self.session.query(UserEntity).filter(UserEntity.id == user_id).delete()
        self.session.commit()

    def login(self, email: str, password: str):
        user = (
            self.session.query(UserEntity)
            .filter(
                UserEntity.email == email,
                UserEntity.password == password,
            )
            .first()
        )
        return user

    def validate_username(self, username: str) -> bool:
        username_exists = (
            self.session.query(UserEntity)
            .filter(
                UserEntity.username == username,
            )
            .first()
        )
        if not username_exists:
            return False

        return True

    def validate_email(self, email: str):
        email_exists = (
            self.session.query(UserEntity)
            .filter(
                UserEntity.email == email,
            )
            .first()
        )
        if not email_exists:
            return False

        return True
