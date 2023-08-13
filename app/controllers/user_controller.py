"""Card Controller."""
from datetime import datetime
from typing import List, Optional, Union

from sqlalchemy import or_

from app.connections.mysql.models.mysql_user import MySQLUser
from app.dependencies import Dependencies
from app.models.users.user import User


class UserController:
    """Classe para gerenciamento dos Cards."""

    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database

    def validate_username_exists(self, username: str):
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
            raise error

    def validate_user_exists(self, user: User):
        """Validação se já existe um usuário com mesmo Email ou Username

        Args:
            user (User): User a ser inserido

        Returns:

        """
        try:
            session = self.database.session()

            existing_user = (
                session.query(MySQLUser)
                .filter(
                    or_(
                        MySQLUser.email == user.email,
                        MySQLUser.username == user.username,
                    )
                )
                .first()
            )

            return True if existing_user else False

        except Exception as error:
            raise error

    def insert_user(self, user: User):
        """Inserção de um novo Card.

        Args:
            user (User): User a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo Database
        """
        try:
            session = self.database.session()

            mysql_user = MySQLUser(**user.__dict__)
            mysql_user.creation_date = datetime.now()

            session.add(mysql_user)
            session.commit()

            return True

        except Exception as error:
            raise error

    def get_user(self, user_id: int) -> Optional[Union[None, User]]:
        session = self.database.session()

        row = (session.query(MySQLUser).filter(MySQLUser.id == user_id).first())
        if not row:
            return None

        return User(
            id=row.id,
            email=row.email,
            username=row.username,
            password=row.password,
            creation_date=row.creation_date,
        )

    def get_all_users(self) -> List[User]:
        """Busca de todos os Users cadastrados.

        Returns:
            users (list): Lista com todos os Cards
        """
        session = self.database.session()

        rows = session.query(MySQLUser).all()

        users = []
        for row in rows:
            users.append(
                User(
                    id=row.id,
                    email=row.email,
                    username=row.username,
                    password=row.password,
                    creation_date=row.creation_date,
                )
            )

        return users
