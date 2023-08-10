"""Card Controller."""
from app.connections.mongo.mongo_db import MongoDB
from app.models.cards import Card


class CardController:
    """Classe para gerenciamento dos Cards."""

    def __init__(self):
        """Construtor da classe."""
        self.mongo_db = MongoDB()
        self.collection = "Cards"

    def insert_card(self, card: Card):
        """Inserção de um novo Card.

        Args:
            card (Card): Card a ser inserido

        Returns:
            inserted_id (int): ID do registro gerado pelo MongoDB
        """
        collection = self.mongo_db.database[self.collection]
        inserted_id = collection.insert_one(card.__dict__).inserted_id
        return inserted_id

    def get_all_cards(self):
        """Busca de todos os Cards cadastrados.

        Returns:
            cards (list): Lista com todos os Cards
        """
        documents = self.mongo_db.find_documents(collection_name="Cards")
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
