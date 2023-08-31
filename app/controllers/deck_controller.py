"""Deck Controller."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.connections.dependencies import Dependencies
from app.connections.mysql.models.mysql_deck import MySQLDeck
from app.connections.mysql.models.mysql_subdeck import MySQLSubDeck
from app.models.cards.card import Card
from app.models.decks.deck import Deck
from app.models.subdecks.subdeck import SubDeck
from app.utils.errors import (DatabaseDeleteFailed, DatabaseInsertFailed,
                              DatabaseQueryFailed)


class DeckController:
    """Class for managing Decks."""

    def __init__(self, db_conn):
        """Constructor of the class.

        Args:
            db_conn (): Database connection object.
        """
        self.database = db_conn

    def insert_deck(self, deck: Deck) -> Deck:
        """Insert a new Deck into the database.

        Args:
            deck (Deck): Deck to be inserted.

        Returns:
            Deck: The inserted Deck with updated properties.
        """
        try:
            with self.database.session() as session:
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
        """Delete a Deck from the database.

        Args:
            deck_id (int): ID of the Deck to be deleted.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            with self.database.session() as session:
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
        """Retrieve all Decks from the database.

        Returns:
            List[Deck]: List of all Decks with associated SubDecks and Cards.
        """
        try:
            with self.database.session() as session:
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
        """Check if a Deck with the given ID exists in the database.

        Args:
            deck_id (int): ID of the Deck to check.

        Returns:
            bool: True if the Deck exists, False otherwise.
        """
        try:
            with self.database.session() as session:
                existing_deck = (
                    session.query(MySQLDeck).filter(MySQLDeck.id == deck_id).first()
                )

            return True if existing_deck else False

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def get_deck(self, deck_id: int) -> Optional[Deck]:
        """Retrieve a Deck with the given ID from the database.

        Args:
            deck_id (int): ID of the Deck to retrieve.

        Returns:
            Optional[Deck]: The retrieved Deck with associated SubDecks and Cards,
                           or None if the Deck doesn't exist.
        """
        try:
            with self.database.session() as session:
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

    def get_deck_subdecks(self, deck_id: int) -> Optional[List[SubDeck]]:
        """

        Args:
            deck_id (int): Deck ID

        Returns:
            Optional[List[SubDeck]]:
        """
        try:
            with self.database.session() as session:
                subdecks = (
                    session.query(MySQLSubDeck)
                    .filter(MySQLSubDeck.deck_id == deck_id)
                    .all()
                )

                if not subdecks:
                    return None

            subdecks_list = []
            for subdeck in subdecks:
                subdecks_list.append(SubDeck(
                    id=subdeck.id,
                    name=subdeck.name,
                    description=subdeck.description,
                    creation_date=subdeck.creation_date
                ))

            return subdecks_list
        except Exception as error:
            raise DatabaseQueryFailed(error)

    @staticmethod
    def map_subdecks_and_cards(subdecks: List[MySQLSubDeck]) -> List[SubDeck]:
        """Map MySQLSubDeck objects to SubDeck objects with associated Cards.

        Args:
            subdecks (List[MySQLSubDeck]): List of MySQLSubDeck objects.

        Returns:
            List[SubDeck]: List of SubDeck objects with associated Cards.
        """
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
