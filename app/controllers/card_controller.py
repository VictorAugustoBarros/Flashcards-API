"""Card Controller."""
from datetime import datetime
from typing import Optional

from app.connections.mysql.models.mysql_card import MySQLCard
from app.models.cards.card import Card
from app.utils.dependencies import Dependencies


class CardController:
    """Classe para gerenciamento dos Cards."""

    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database

    def insert_card(self, card: Card, subdeck_id: int):
        """Inserção de um novo Card.

        Args:
            card (Card): Card a ser inserido
            subdeck_id (Int): Card a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        try:
            session = self.database.session()

            mysql_card = MySQLCard(**card.__dict__)
            mysql_card.subdeck_id = subdeck_id
            mysql_card.creation_date = datetime.now()

            session.add(mysql_card)
            session.commit()

            return True

        except Exception as error:
            raise error

    def get_all_cards(self):
        """Busca de todos os Cards cadastrados.

        Returns:
            cards (list): Lista com todos os Cards
        """
        session = self.database.session()

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

    def get_card(self, card_id: int) -> Optional[Card]:
        """Função resolve para busca do Card por ID

        Args:
            card_id (int): ID do Card

        Returns:
            card(Card): Card encontrado
        """
        session = self.database.session()

        card = session.query(MySQLCard).filter(MySQLCard.id == card_id).first()
        if not card:
            return None

        return Card(
            id=card.id,
            question=card.question,
            answer=card.answer,
            creation_date=card.creation_date,
        )
