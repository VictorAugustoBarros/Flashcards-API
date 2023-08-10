"""Card Controller."""
from typing import Optional, Union

from app.dependencies import get_database
from app.models.cards import Card


class CardController:
    """Classe para gerenciamento dos Cards."""

    def __init__(self):
        """Construtor da classe."""
        self.database = get_database()
        self.collection = "Cards"

    def insert_card(self, card: Card):
        """Inserção de um novo Card.

        Args:
            card (Card): Card a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        inserted_id = self.database.insert_document(
            collection_name=self.collection, document=card.__dict__
        )
        return inserted_id

    def get_question(self, question: str) -> Optional[Union[Card, None]]:
        """Busca de um Card pela variavel *question*

        Args:
            question (str): Question a ser pesquisada

        Returns:
            cards (List[Cards]): lista com os cards encontrados
        """
        document = self.database.find_one_document(
            collection_name=self.collection, mongo_query={"question": question}
        )
        if not document:
            return None

        return Card(
            question=document.get("question"),
            answer=document.get("answer"),
            insert_date=document.get("insert_date"),
            additional_info=document.get("additional_info"),
        )

    def get_all_cards(self):
        """Busca de todos os Cards cadastrados.

        Returns:
            cards (list): Lista com todos os Cards
        """
        documents = self.database.find_documents(collection_name="Cards")
        cards = []
        for document in documents:
            cards.append(
                Card(
                    question=document.get("question"),
                    answer=document.get("answer"),
                    insert_date=document.get("insert_date"),
                    additional_info=document.get("additional_info"),
                )
            )

        return cards
