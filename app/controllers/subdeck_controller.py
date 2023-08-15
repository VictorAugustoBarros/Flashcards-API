"""SubDeck Controller."""
from datetime import datetime

from sqlalchemy.orm import joinedload

from app.connections.mysql.models.mysql_subdeck import MySQLSubDeck
from app.models.cards.card import Card
from app.models.subdecks.subdeck import SubDeck
from app.utils.dependencies import Dependencies


class SubDeckController:
    """Classe para gerenciamento dos SubDeck."""

    def __init__(self):
        """Construtor da classe."""
        self.database = Dependencies.database

    def insert_subdeck(self, subdeck: SubDeck, deck_id: int) -> SubDeck:
        """Inserção de um novo SubDeck.

        Args:
            subdeck (SubDeck): SubDeck a ser cadastrado
            deck_id (int): ID do Deck a ser cadastrado

        Returns:
            subdeck (SubDeck): SubDeck com os dados atualizados
        """
        try:
            session = self.database.session()

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
            raise error

    def get_subdeck(self, subdeck_id: int):
        session = self.database.session()

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

    def get_all_subdecks(self):
        """Busca de todos os SubDecks cadastrados.

        Returns:
            subdecks (list): Lista com todos os Decks
        """
        session = self.database.session()

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

    def validate_subdeck_exists(self, subdeck_id: int) -> bool:
        session = self.database.session()

        existing_subdeck = (
            session.query(MySQLSubDeck).filter(MySQLSubDeck.id == subdeck_id).first()
        )

        return True if existing_subdeck else False
