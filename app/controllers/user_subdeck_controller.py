from datetime import datetime

from sqlalchemy import and_

from app.connections.mysql.models.mysql_user_subdeck import MySQLUserSubDeck
from app.controllers.subdeck_controller import SubDeckController
from app.utils.dependencies import Dependencies



class UserSubDeckController:
    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database
        self.subdeck_controller = SubDeckController()

    def insert_user_subdeck(self, user_id: int, subdeck_id: int):
        try:
            session = self.database.session()

            mysql_user_sub_deck = MySQLUserSubDeck()
            mysql_user_sub_deck.user_id = user_id
            mysql_user_sub_deck.subdeck_id = subdeck_id
            mysql_user_sub_deck.creation_date = datetime.now()

            session.add(mysql_user_sub_deck)
            session.commit()

            return True

        except Exception as error:
            raise error

    def validate_link_userdeck_exists(self, user_id: int, subdeck_id: int) -> bool:
        session = self.database.session()

        existing_usersubdeck = session.query(MySQLUserSubDeck).filter(
            and_(
                MySQLUserSubDeck.user_id == user_id,
                MySQLUserSubDeck.subdeck_id == subdeck_id
            )
        ).first()

        return True if existing_usersubdeck else False

    def get_user_subdeck(self, user_id: int):
        try:
            session = self.database.session()

            user_subdecks = (
                session.query(MySQLUserSubDeck)
                .filter(MySQLUserSubDeck.user_id == user_id)
                .all()
            )

            decks = []
            for user_subdeck in user_subdecks:
                decks.append(self.subdeck_controller.get_subdeck(subdeck_id=user_subdeck.subdeck.id))

            return decks

        except Exception as error:
            raise error