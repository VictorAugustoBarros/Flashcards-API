"""Card Controller."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_

from app.graphql_config.cards import Card
from app.utils.errors import (
    DatabaseInsertFailed,
    DatabaseQueryFailed,
    DatabaseUpdateFailed,
)


class CardController:
    """Classe para gerenciamento dos Cards."""

    def __init__(self, db_conn):
        """Construtor da classe."""
        self.database = db_conn

    def insert_card(self, card: Card, subdeck_id: int) -> Card:
        """Inserção de um novo Card.

        Args:
            card (Card): Card a ser inserido
            subdeck_id (Int): Card a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        try:
            with self.database.session() as session:
                mysql_card = MySQLCard(**card.__dict__)
                mysql_card.subdeck_id = subdeck_id
                mysql_card.creation_date = datetime.now()

                session.add(mysql_card)
                session.commit()

                card.id = mysql_card.id
                card.creation_date = mysql_card.creation_date

            return card

        except Exception as error:
            raise DatabaseInsertFailed(error)

    def delete_card(self, card_id: int) -> bool:
        try:
            with self.database.session() as session:
                session.query(MySQLCard).filter(MySQLCard.id == card_id).delete()
                session.commit()

            return True

        except Exception as error:
            raise DatabaseInsertFailed(error)

    def update_card(self, card_id: int, question: str, answer: str) -> bool:
        try:
            with self.database.session() as session:
                card = session.query(MySQLCard).filter(MySQLCard.id == card_id).first()
                if not card:
                    return False

                card.question = question
                card.answer = answer
                session.commit()

            return True

        except Exception as error:
            raise DatabaseUpdateFailed(error)

    def get_all_cards(self) -> List[Card]:
        """Busca de todos os Cards cadastrados.

        Returns:
            cards (list): Lista com todos os Cards
        """
        try:
            with self.database.session() as session:
                cards = session.query(MySQLCard).all()

                all_cards = []
                for card in cards:
                    all_cards.append(
                        Card(
                            id=card.id,
                            question=card.question,
                            answer=card.answer,
                            creation_date=card.creation_date,
                        )
                    )

            return all_cards

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def get_card(self, card_id: int) -> Optional[Card]:
        """Função resolve para busca do Card por ID

        Args:
            card_id (int): ID do Card

        Returns:
            card(Card): Card encontrado
        """
        try:
            with self.database.session() as session:
                card = session.query(MySQLCard).filter(MySQLCard.id == card_id).first()
                if not card:
                    return None

            return Card(
                id=card.id,
                question=card.question,
                answer=card.answer,
                creation_date=card.creation_date,
            )

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def get_subdeck_cards(self, subdeck_id: int) -> Optional[List[Card]]:
        """Função resolve para busca do Card por ID

        Args:
            subdeck_id (int): ID do Subdeck

        Returns:
            card(Card): Card encontrado
        """
        try:
            with self.database.session() as session:
                cards = (
                    session.query(MySQLCard)
                    .filter(MySQLCard.subdeck_id == subdeck_id)
                    .all()
                )
                if not cards:
                    return None

            cards_list = []
            for card in cards:
                cards_list.append(
                    Card(
                        id=card.id,
                        question=card.question,
                        answer=card.answer,
                        creation_date=card.creation_date,
                    )
                )

            return cards_list

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def is_card_user(self, card_id: int, user_id: int):
        try:
            with self.database.session() as session:
                result = (
                    session.query(MySQLCard)
                    .join(MySQLSubDeck)
                    .join(MySQLDeck)
                    .join(MySQLUserDeck)
                    .filter(
                        and_(MySQLUserDeck.user_id == user_id, MySQLCard.id == card_id)
                    )
                    .first()
                )
            if not result:
                return False

            return True

        except Exception as error:
            raise DatabaseQueryFailed(error)
