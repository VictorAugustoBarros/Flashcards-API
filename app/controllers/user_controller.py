"""Card Controller."""
from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy import or_

from app.connections.mysql.models.mysql_user import MySQLUser
from app.models.users.user import User
from app.utils.errors import (
    DatabaseInsertFailed,
    DatabaseQueryFailed,
    DatabaseDeleteFailed,
)


class UserController:
    """Classe para gerenciamento dos Cards."""

    def __init__(self, db_conn):
        """Construtor da classe."""
        self.database = db_conn

    def insert_user(self, user: User) -> User:
        """Inserção de um novo Card.

        Args:
            user (User): User a ser inserido

        Returns:
            user (User): User com os dados atualizados
        """
        try:
            session = self.database.session()

            mysql_user = MySQLUser(**user.__dict__)
            mysql_user.creation_date = datetime.now()

            session.add(mysql_user)
            session.commit()

            user.id = mysql_user.id
            user.creation_date = mysql_user.creation_date

            return user

        except Exception as error:
            raise DatabaseInsertFailed(error)

    def validate_username_exists(self, username: str) -> bool:
        try:
            session = self.database.session()

            existing_username = (
                session.query(MySQLUser)
                .filter(
                    MySQLUser.username == username,
                )
                .first()
            )

            return True if existing_username else False

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def validate_user_exists(self, user_id: int) -> bool:
        try:
            session = self.database.session()

            existing_user = (
                session.query(MySQLUser).filter(MySQLUser.id == user_id).first()
            )

            return True if existing_user else False

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def validate_user_email_username_exists(self, email: str, username: str) -> bool:
        """Validação se já existe um usuário com mesmo Email ou Username

        Args:
            email (str): Email do usuário
            username (str): Username do usuário

        Returns:
            existing_user(bool):
                True -> Email e Username já existem
                Fasle -> Email e Username disponíveis
        """
        try:
            session = self.database.session()

            existing_user = (
                session.query(MySQLUser)
                .filter(
                    or_(
                        MySQLUser.email == email,
                        MySQLUser.username == username,
                    )
                )
                .first()
            )

            return True if existing_user else False

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def get_user(self, user_id: int) -> Optional[User]:
        try:
            session = self.database.session()

            user = session.query(MySQLUser).filter(MySQLUser.id == user_id).first()
            if not user:
                return None

            return User(
                id=user.id,
                email=user.email,
                username=user.username,
                password=user.password,
                creation_date=user.creation_date,
            )

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def get_all_users(self) -> List[User]:
        """Busca de todos os Users cadastrados.

        Returns:
            users (list): Lista com todos os Cards
        """
        try:
            session = self.database.session()

            users = session.query(MySQLUser).all()

            all_users = []
            for user in users:
                all_users.append(
                    User(
                        id=user.id,
                        email=user.email,
                        username=user.username,
                        password=user.password,
                        creation_date=user.creation_date,
                    )
                )

            return all_users

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def delete_user(self, user_id: int) -> bool:
        try:
            session = self.database.session()
            existing_user = (
                session.query(MySQLUser).filter(MySQLUser.id == user_id).first()
            )
            if existing_user:
                session.delete(existing_user)
                session.commit()
                return True

            return False

        except Exception as error:
            raise DatabaseDeleteFailed(error)
