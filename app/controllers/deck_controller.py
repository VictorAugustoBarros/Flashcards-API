"""Deck Controller."""
from datetime import datetime

from sqlalchemy.orm import joinedload
from sqlalchemy.orm.collections import InstrumentedList

from app.connections.mysql.models.mysql_deck import MySQLDeck
from app.connections.mysql.models.mysql_subdeck import MySQLSubDeck
from app.dependencies import Dependencies
from app.models.cards.card import Card
from app.models.decks.deck import Deck
from app.models.subdecks.subdeck import SubDeck


class DeckController:
    """Classe para gerenciamento dos Deck."""

    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database
        self.collection = "Decks"

    def insert_deck(self, deck: Deck):
        """Inserção de um novo Deck.

        Args:
            deck (Deck): Deck a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        try:
            session = self.database.session()

            mysql_deck = MySQLDeck(**deck.__dict__)
            mysql_deck.creation_date = datetime.now()

            session.add(mysql_deck)
            session.commit()

            return True

        except Exception as error:
            raise error

    def get_all_decks(self):
        session = self.database.session()

        rows = (
            session.query(MySQLDeck)
            .options(
                joinedload(MySQLDeck.subdecks, innerjoin=True).joinedload(
                    MySQLSubDeck.cards
                )
            )
            .all()
        )

        decks = []
        for row in rows:
            sub_decks = self.map_subdecks_and_cards(row.subdecks)
            decks.append(
                Deck(
                    id=row.id,
                    name=row.name,
                    description=row.description,
                    creation_date=row.creation_date,
                    sub_deck=sub_decks,
                )
            )

        return decks

    def get_deck(self, deck_id: int):
        session = self.database.session()

        row = (
            session.query(MySQLDeck)
            .filter(MySQLDeck.id == deck_id)
            .options(
                joinedload(MySQLDeck.subdecks, innerjoin=True).joinedload(
                    MySQLSubDeck.cards
                )
            )
            .first()
        )

        if not row:
            return None

        sub_decks = self.map_subdecks_and_cards(row.subdecks)
        return Deck(
            id=row.id,
            name=row.name,
            description=row.description,
            creation_date=row.creation_date,
            sub_deck=sub_decks,
        )

    @staticmethod
    def map_subdecks_and_cards(subdecks: InstrumentedList[MySQLSubDeck]):
        mapped_subdecks = []
        for sub_deck in subdecks:
            cards = []
            for card in sub_deck.cards:
                cards.append(
                    Card(
                        id=card.id,
                        question=card.question,
                        answer=card.answer,
                        creation_date=card.creation_date,
                    )
                )

            mapped_subdecks.append(
                SubDeck(
                    id=sub_deck.id,
                    name=sub_deck.name,
                    description=sub_deck.description,
                    creation_date=sub_deck.creation_date,
                    cards=cards,
                )
            )
        return mapped_subdecks
