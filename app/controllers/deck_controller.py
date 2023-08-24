"""Deck Controller."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.collections import InstrumentedList

from app.connections.dependencies import Dependencies
from app.connections.mysql.models.mysql_deck import MySQLDeck
from app.connections.mysql.models.mysql_subdeck import MySQLSubDeck
from app.models.cards.card import Card
from app.models.decks.deck import Deck
from app.models.subdecks.subdeck import SubDeck
from app.utils.errors import (DatabaseDeleteFailed, DatabaseInsertFailed,
                              DatabaseQueryFailed)


class DeckController:
    """Classe para gerenciamento dos Deck."""

    def __init__(self, db_conn):
        """Construtor da classe."""
        self.database = db_conn

    def insert_deck(self, deck: Deck) -> Deck:
        """Inserção de um novo Deck.

        Args:
            deck (Deck): Deck a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        try:
            session = self.database.session()

            mysql_deck = MySQLDeck(
                id=deck.id,
                name=deck.name,
                description=deck.description,
            )
            mysql_deck.creation_date = datetime.now()

            session.add(mysql_deck)
            session.commit()
            deck.id = mysql_deck.id
            deck.creation_date = mysql_deck.creation_date

            return deck

        except Exception as error:
            raise DatabaseInsertFailed(error)

    def delete_deck(self, deck_id: int) -> bool:
        try:
            session = self.database.session()
            existing_deck = (
                session.query(MySQLDeck).filter(MySQLDeck.id == deck_id).first()
            )
            if existing_deck:
                session.delete(existing_deck)
                session.commit()
                return True

            return False

        except Exception as error:
            raise DatabaseDeleteFailed(error)

    def get_all_decks(self) -> List[Deck]:
        try:
            session = self.database.session()

            decks = (
                session.query(MySQLDeck)
                .options(
                    joinedload(MySQLDeck.subdecks, innerjoin=False).joinedload(
                        MySQLSubDeck.cards
                    )
                )
                .all()
            )

            all_decks = []
            for deck in decks:
                sub_decks = self.map_subdecks_and_cards(deck.subdecks)
                all_decks.append(
                    Deck(
                        id=deck.id,
                        name=deck.name,
                        description=deck.description,
                        creation_date=deck.creation_date,
                        sub_deck=sub_decks,
                    )
                )

            return all_decks

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def validate_deck_exists(self, deck_id: int) -> bool:
        try:
            session = self.database.session()

            existing_deck = (
                session.query(MySQLDeck).filter(MySQLDeck.id == deck_id).first()
            )

            return True if existing_deck else False

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def get_deck(self, deck_id: int) -> Optional[Deck]:
        try:
            session = self.database.session()

            deck = (
                session.query(MySQLDeck)
                .filter(MySQLDeck.id == deck_id)
                .options(
                    joinedload(MySQLDeck.subdecks, innerjoin=False).joinedload(
                        MySQLSubDeck.cards
                    )
                )
                .first()
            )

            if not deck:
                return None

            sub_decks = self.map_subdecks_and_cards(deck.subdecks)
            return Deck(
                id=deck.id,
                name=deck.name,
                description=deck.description,
                creation_date=deck.creation_date,
                sub_deck=sub_decks,
            )

        except Exception as error:
            raise DatabaseQueryFailed(error)

    @staticmethod
    def map_subdecks_and_cards(
        subdecks: List[MySQLSubDeck],
    ) -> List[SubDeck]:
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
