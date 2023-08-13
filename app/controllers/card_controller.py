"""Card Controller."""
from datetime import datetime

from app.connections.mysql.models.mysql_card import MySQLCard
from app.dependencies import Dependencies
from app.models.cards.card import Card


class CardController:
    """Classe para gerenciamento dos Cards."""

    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database
        self.collection = "Cards"

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

        rows = session.query(MySQLCard).all()

        cards = []
        for row in rows:
            cards.append(
                Card(
                    id=row.id,
                    question=row.question,
                    answer=row.answer,
                    creation_date=row.creation_date,
                )
            )

        return cards

    def get_card(self, card_id: int):
        session = self.database.session()

        row = (
            session.query(MySQLCard)
            .filter(MySQLCard.id == card_id)
            .first()
        )

        if not row:
            return None

        return Card(
            id=row.id,
            question=row.question,
            answer=row.answer,
            creation_date=row.creation_date,
        )
