"""User Deck Controller."""
from datetime import datetime
from typing import List

from sqlalchemy import and_

from app.connections.mysql.models.mysql_user_deck import MySQLUserDeck
from app.controllers.deck_controller import DeckController
from app.models.decks.deck import Deck
from app.utils.dependencies import Dependencies


class UserDeckController:
    """Classe para controle do UserDeck."""

    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database
        self.deck_controller = DeckController()

    def insert_user_deck(self, user_id: int, deck_id: int) -> bool:
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

            return True

        except Exception as error:
            raise error

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
                decks.append(self.deck_controller.get_deck(deck_id=user_deck.deck.id))

            return decks

        except Exception as error:
            raise error

    def validate_link_userdeck_exists(self, user_id: int, deck_id: int) -> bool:
        List[Deck]
        session = self.database.session()

        existing_userdeck = (
            session.query(MySQLUserDeck)
            .filter(
                and_(MySQLUserDeck.user_id == user_id, MySQLUserDeck.deck_id == deck_id)
            )
            .first()
        )

        return True if existing_userdeck else False
