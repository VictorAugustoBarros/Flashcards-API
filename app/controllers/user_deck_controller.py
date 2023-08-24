"""User Deck Controller."""
from datetime import datetime
from typing import List

from sqlalchemy import and_

from app.connections.dependencies import Dependencies
from app.connections.mysql.models.mysql_user_deck import MySQLUserDeck
from app.controllers.deck_controller import DeckController
from app.models.decks.deck import Deck
from app.models.user_deck.user_deck import UserDeck
from app.utils.errors import (DatabaseDeleteFailed, DatabaseInsertFailed,
                              DatabaseQueryFailed)


class UserDeckController:
    """Classe para controle do UserDeck."""

    def __init__(self, db_conn):
        """Construtor da classe."""
        self.database = db_conn
        self.deck_controller = DeckController(db_conn=db_conn)

    def insert_user_deck(self, user_id: int, deck_id: int) -> UserDeck:
        """Inserção de um novo Deck

        Args:
            user_id(int): ID do Usuário
            deck_id(int): ID do Deck

        Returns:

        """
        try:
            session = self.database.session()

            mysql_user_deck = MySQLUserDeck()
            mysql_user_deck.user_id = user_id
            mysql_user_deck.deck_id = deck_id
            mysql_user_deck.creation_date = datetime.now()

            session.add(mysql_user_deck)
            session.commit()

            return UserDeck(
                id=mysql_user_deck.id,
                user_id=user_id,
                deck_id=deck_id,
            )

        except Exception as error:
            raise DatabaseInsertFailed(error)

    def get_user_deck(self, user_id: int) -> List[Deck]:
        """Busca dos decks cadastrados do usuário

        Args:
            user_id: ID do usuário

        Returns:
            List[Deck]: Lista com os Decks cadastrados
        """
        try:
            session = self.database.session()

            user_decks = (
                session.query(MySQLUserDeck)
                .filter(MySQLUserDeck.user_id == user_id)
                .all()
            )

            decks = []
            for user_deck in user_decks:
                deck = self.deck_controller.get_deck(deck_id=user_deck.deck.id)
                decks.append(deck)

            return decks

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def validate_link_userdeck_exists(self, user_id: int, deck_id: int) -> bool:
        try:
            session = self.database.session()

            existing_userdeck = (
                session.query(MySQLUserDeck)
                .filter(
                    and_(
                        MySQLUserDeck.user_id == user_id,
                        MySQLUserDeck.deck_id == deck_id,
                    )
                )
                .first()
            )

            return True if existing_userdeck else False

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def delete_user_deck(self, user_deck_id: int) -> bool:
        try:
            session = self.database.session()
            existing_user_deck = (
                session.query(MySQLUserDeck)
                .filter(MySQLUserDeck.id == user_deck_id)
                .first()
            )
            if existing_user_deck:
                session.delete(existing_user_deck)
                session.commit()
                return True

            return False

        except Exception as error:
            raise DatabaseDeleteFailed(error)
