"""SubDeck Controller."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import joinedload

from app.graphql_config.cards import Card
from app.models.subdeck import SubDeck
from app.utils.errors import (
    DatabaseDeleteFailed,
    DatabaseInsertFailed,
    DatabaseQueryFailed,
)


class SubDeckController:
    """Classe para gerenciamento dos SubDeck."""

    def __init__(self, db_conn):
        """Construtor da classe."""
        self.database = db_conn

    def insert_subdeck(self, subdeck: SubDeck, deck_id: int) -> SubDeck:
        """Inserção de um novo SubDeck.

        Args:
            subdeck (SubDeck): SubDeck a ser cadastrado
            deck_id (int): ID do Deck a ser cadastrado

        Returns:
            subdeck (SubDeck): SubDeck com os dados atualizados
        """
        try:
            with self.database.session() as session:
                mysql_subdeck = MySQLSubDeck(
                    name=subdeck.name, description=subdeck.description, deck_id=deck_id
                )
                mysql_subdeck.creation_date = datetime.now()

                session.add(mysql_subdeck)
                session.commit()
                subdeck.id = mysql_subdeck.id
                subdeck.creation_date = mysql_subdeck.creation_date

            return subdeck

        except Exception as error:
            raise DatabaseInsertFailed(error)

    def delete_subdeck(self, subdeck_id: int) -> bool:
        try:
            with self.database.session() as session:
                existing_subdeck = (
                    session.query(MySQLSubDeck)
                    .filter(MySQLSubDeck.id == subdeck_id)
                    .first()
                )
                if existing_subdeck:
                    session.delete(existing_subdeck)
                    session.commit()
                    return True

            return False

        except Exception as error:
            raise DatabaseDeleteFailed(error)

    def get_subdeck(self, subdeck_id: int) -> Optional[SubDeck]:
        try:
            with self.database.session() as session:
                subdeck = (
                    session.query(MySQLSubDeck)
                    .filter(MySQLSubDeck.id == subdeck_id)
                    .options(joinedload(MySQLSubDeck.cards, innerjoin=False))
                    .first()
                )
                if not subdeck:
                    return None

            cards = []
            for card in subdeck.cards:
                cards.append(
                    Card(
                        id=card.id,
                        question=card.question,
                        answer=card.answer,
                        creation_date=card.creation_date,
                    )
                )

            return SubDeck(
                id=subdeck.id,
                name=subdeck.name,
                description=subdeck.description,
                creation_date=subdeck.creation_date,
                cards=cards,
            )

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def get_all_subdecks(self) -> List[SubDeck]:
        """Busca de todos os SubDecks cadastrados.

        Returns:
            subdecks (list): Lista com todos os Decks
        """
        try:
            with self.database.session() as session:
                subdecks = (
                    session.query(MySQLSubDeck)
                    .options(joinedload(MySQLSubDeck.cards, innerjoin=False))
                    .all()
                )

                all_subdecks = []
                for subdeck in subdecks:
                    cards = []
                    for card in subdeck.cards:
                        cards.append(
                            Card(
                                id=card.id,
                                question=card.question,
                                answer=card.answer,
                                creation_date=card.creation_date,
                            )
                        )

                    all_subdecks.append(
                        SubDeck(
                            id=subdeck.id,
                            name=subdeck.name,
                            description=subdeck.description,
                            creation_date=subdeck.creation_date,
                            cards=cards,
                        )
                    )

            return all_subdecks

        except Exception as error:
            raise DatabaseQueryFailed(error)

    def validate_subdeck_exists(self, subdeck_id: int) -> bool:
        try:
            with self.database.session() as session:
                existing_subdeck = (
                    session.query(MySQLSubDeck)
                    .filter(MySQLSubDeck.id == subdeck_id)
                    .first()
                )

            return True if existing_subdeck else False

        except Exception as error:
            raise DatabaseQueryFailed(error)
