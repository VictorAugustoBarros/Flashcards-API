"""SubDeck Controller."""
from datetime import datetime

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.collections import InstrumentedList

from app.connections.mysql.models.mysql_subdeck import MySQLSubDeck
from app.connections.mysql.models.mysql_card import MySQLCard
from app.dependencies import Dependencies
from app.models.cards.card import Card
from app.models.subdecks.subdeck import SubDeck


class SubDeckController:
    """Classe para gerenciamento dos SubDeck."""

    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database

    def insert_subdeck(self, subdeck: SubDeck, deck_id: int):
        """Inserção de um novo SubDeck.

        Args:
            subdeck (SubDeck): Deck a ser inserido
            deck_id (int): ID do deck a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo database
        """
        try:
            session = self.database.session()

            mysql_subdeck = MySQLSubDeck(
                name=subdeck.name, description=subdeck.description, deck_id=deck_id
            )
            mysql_subdeck.creation_date = datetime.now()

            session.add(mysql_subdeck)
            session.commit()

            return True

        except Exception as error:
            raise error

    def get_subdeck(self, subdeck_id: int):
        session = self.database.session()

        row = (
            session.query(MySQLSubDeck)
            .filter(MySQLSubDeck.id == subdeck_id)
            .options(
                joinedload(MySQLSubDeck.cards, innerjoin=True)
            )
            .first()
        )
        if not row:
            return None

        cards = []
        for card in row.cards:
            cards.append(
                Card(
                    id=card.id,
                    question=card.question,
                    answer=card.answer,
                    creation_date=card.creation_date,
                )
            )

        return SubDeck(
            id=row.id,
            name=row.name,
            description=row.description,
            creation_date=row.creation_date,
            cards=cards,
        )

    def get_all_subdecks(self):
        """Busca de todos os SubDecks cadastrados.

        Returns:
            subdecks (list): Lista com todos os Decks
        """
        session = self.database.session()

        rows = (
            session.query(MySQLSubDeck)
            .options(
                joinedload(MySQLSubDeck.cards, innerjoin=True)
            )
            .all()
        )

        decks = []
        for row in rows:
            cards = []
            for card in row.cards:
                cards.append(
                    Card(
                        id=card.id,
                        question=card.question,
                        answer=card.answer,
                        creation_date=card.creation_date,
                    )
                )

            decks.append(
                SubDeck(
                    id=row.id,
                    name=row.name,
                    description=row.description,
                    creation_date=row.creation_date,
                    cards=cards,
                )
            )

        return decks
